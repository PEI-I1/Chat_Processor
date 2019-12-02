from categoria_dic import cat as dicionario
from spell_checker import spell_check_ss
from utils import *
import globals, nltk, json
import regex as re

confianca_level = 0.70
tries = 5

# remove stopwords e pontuação da mensagem recebida como input
# retorna uma lista com as palavras
def limpa_texto(mensagem):
    mensagem = nltk.word_tokenize(mensagem.lower())
    mensagem = [palavra for palavra in mensagem if palavra not in nltk.corpus.stopwords.words('portuguese') and not re.match('\p{punct}', palavra)]
    return mensagem

# cria um dic 'noccur' com o número de occorências na frase para cada categoria
def criar_noccur_dic(palavras):
    noccur = {}
    for pal in palavras:
        for cat in dicionario:
            for word in cat['words']:
                if word == pal:
                    noccur[cat['request']] = noccur.get(cat['request'], 0) + 1
    return noccur

# com base na dic do noccur calcular qual é a categoria mais provável e a sua confiança
# confiança = noccur da categoria que aparece mais / número de ocorrência de todas as categorias
def calcula_confianca(noccur):
    total = 0
    confianca = 0
    if len(noccur):
        cat_maior = max(noccur, key=noccur.get)
        valor_cat = noccur.get(cat_maior)

        for valor in noccur.values():
            total += valor

        confianca = valor_cat / total
    else:
        cat_maior = "Not Found"
        confianca = 0
    return cat_maior,confianca

def get_categoria_frase(inp):
    inp = spell_check_ss(inp)
    palavras = limpa_texto(inp)
    noccur = criar_noccur_dic(palavras)
    return calcula_confianca(noccur)


def proc_ents(inp):
    words = inp[0][0]
    ents = inp[1][0]

    i = 0
    w = ""
    t = ""
    ret = []
    while i < len(words):
        if ents[i] != "O":
            if ents[i][0] == 'B':
                if w != "":
                    ret.append({'entity': w, 'type': t})
                w = words[i]
                t = ents[i][2:]
            else:
                w += " " + words[i]
        i+=1

    if w != "":
        ret.append({'entity': w, 'type': t})

    return ret

# compara os params da frase (msg_params) com os da dic (params)
def compare_params(msg_params,params,db_params):
    required_params = {}

    required_params.append(db_params)

    for (n, t) in params.items():
        if not required_params.get(n,None):
            found = None
            for pp in msg_params:
                if pp.type == t:
                    found = {n:{"type":t,"entity":pp.entity}}

            if not found:
                found = {n:{"type":t}}

            required_params.append(found)

    return required_params

# compara os params da frase (msg_params) com os da dic (required_params)
# def compare_optional_params(msg_params, optional_params):
#     optional_params = {}

#     for (n, t) in optional_params.items():
#         found = None
#         for pp in msg_params:
#             if pp.type == t:
#                 found = {n:{"type":t,"entity":pp.entity}}

#         if not found:
#             found = {n:{"type":t}}

#         optional_params.append(found)

#     return optional_params


# compara os params da frase (msg_params) com os optionais da dic (optional_params)
# def compare_optional_params(msg_params, optional_params):
#     tuplo_optional_params = []

#     for (n, t) in optional_params.items():
#         found = None
#         for pp in msg_params:
#             if pp.type == t:
#                 found = tuple((n,t,pp.entity))

#         tuplo_optional_params.append(found)

#     return tuplo_optional_params

# compara os params da frase (msg_params) com os locations params da dic (tuplo_location_params)
# def compara_location_params(msg_params,location_params):
#     tuplo_location_params = []

#     for p in msg_params:
#         if 'GPE' == p.type:
#             search_term = tuple(('search_term',p.type,p.entity))
#         # if 'lat' == p.type:
#         #     lat = tuple(('lat',p.entity))
#         # if 'lon' == p.type:
#         #     lon = tuple(('lon',p.entity))
#     tuplo_location_params.append(search_term)

#     return tuplo_location_params


# com os params válidos e os params para serem perguntados
def separate_params(params):
    valid_params = {}
    missing_params = {}

    for (n,value) in params.items():
        # se tiver entity está validado, senao esta em falta
        if value.get('entity',None):
            valid_params.append({n:value})
        else:
            missing_params.append({n:value})

    return valid_params, missing_params

def add_new_params(l, new_l):
    for p in new_l:
        if len([param for param in l if param == p]) == 0:
            l.append(p)


# TODO checkar se temos alguma coisa na bd conforme fazemos
def process_params(idChat, idUser, msg, name, chatData):
    detected_request = chatData["cat"]
    entry = get_entry(detected_request)
    paramsRequired = entry['paramsRequired']
    paramsOptional = entry['paramsOptional']
    location_params = entry['locationParam']
    needAtLeastOneOptionalParam = entry['needAtLeastOneOptionalParam']
    msg_params = proc_ents(globals.ner_model([msg]))
    content = None

    # quando há parametros
    if len(paramsRequired) or len(paramsOptional) or len(location_params):
        # obrigatórios
        required_params = compare_params(msg_params, paramsRequired,chatData['paramsRequired'])
        valid_required_params, missing_required_params = separate_params(required_params)

        # opcionais
        optional_params = compare_params(msg_params, paramsOptional,chatData['paramsOptional'])
        valid_optional_params, missing_optional_params = separate_params(paramsOptional)

        # adicionar bd
        add_new_params(chatData['paramsRequired'], valid_required_params)
        add_new_params(chatData['paramsOptional'], valid_optional_params)
        globals.redis_db.set(idChat, json.dumps(chatData))

        # quando n falta nenhum param obrigatório e n existem outros
        if len(missing_required_params) == 0 and not len(paramsOptional) and not len(location_params):
            pass

        # quando falta parãmetro obrigatório -> perguntar ao utilizador os parâmetros
        if len(missing_required_params) > 0 and not content:
            content = entry['missingParamsPhrase']

        # se precisarmos de um param optional e não existir nenhum
        if len(valid_optional_params) == 0 and needAtLeastOneOptionalParam is True and not content:
            pass

        # quand n há param obrigatórios mas pode haver params opcionais (ex /scrapper/sessions/by_date)
        if not len(paramsRequired) and len(paramsOptional) and needAtLeastOneOptionalParam is False and not content:
            content = get_content(detected_request, [valid_optional_params], {})

        # # faltam parãmetros de localização ou opcionais
        # if (len(location_params) > 0 or needAtLeastOneOptionalParam is True) and not content:
        #     # TODO ver como vamos saber a distinção entre search e lat/lon
        #     pass
        # else:
        #     # não faltam parâmetros opcionais nem de localização
        #     valid_params = [p[2] for p in chatData['paramsRequired']]
        #     content = get_content(detected_request, valid_params,{})
        #     globals.redis_db.delete(idChat)

    else:
        content = get_content(detected_request, [], {})
        globals.redis_db.delete(idChat)

    #se for uma lista devolve de forma diferente
    if content:
        if isinstance(content, list):
            msg_send = process_list(content)
            globals.redis_db.set("vermais" + idChat, json.dumps(content))
        else:
            msg_send = content
    else:
        msg_send = "Não foi possível obter a resposta..."

    return msg_send

def get_response_default(idChat, idUser, msg, name, chatData):
    #Mudar categoria???
    if chatData["status"] == "mudar categoria?":
        mc = clean_msg(msg)

        if mc == "sim":
            chatData["cat"] = chatData["cat_change"]
            chatData["cat_change"] = ""
            globals.redis_db.set(idChat, json.dumps(chatData))

        msg_send = process_params(idChat, idUser, msg, name, chatData)
    else:
        cat, confianca = get_categoria_frase(msg)
        params = proc_ents(globals.ner_model([msg]))

        if chatData["cat"] == "":
            if confianca > confianca_level:
                chatData["cat"] = cat
                globals.redis_db.set(idChat, json.dumps(chatData))
                msg_send = process_params(idChat, idUser, msg, name, chatData)
            else:
                if chatData["tries"] == tries - 1:
                    msg_send = "Desculpe mas não foi possível identificar o que pretende.\n\n"
                    msg_send += "Pode tentar o modo de regras ao escrever 'modo de regras'.\n\n"
                    msg_send += "Ou pode se quiser ligar para uma das seguintes linhas de apoio:\n"
                    #TODO: tentar melhorar as linhas de apoio por forma a tentar mostrar apenas o de um assunto
                    linhas_apoio = get_content("linhas_apoio", [], {})
                    if linhas_apoio:
                        msg_send += process_all_list(linhas_apoio)
                    else:
                        msg_send += "Não foi possível obter as linhas de apoio..."
                    globals.redis_db.delete(idChat)
                else:
                    chatData["tries"] += 1
                    globals.redis_db.set(idChat, json.dumps(chatData))
                    msg_send = "Desculpe mas não foi possível identificar o que pretende. Tente de novo!"
        else:
            if confianca > confianca_level:
                if chatData["cat"] == cat:
                    msg_send = process_params(idChat, idUser, msg, name, chatData)
                else:
                    chatData["cat_change"] = cat
                    chatData["paramsRequired"] = params
                    globals.redis_db.set(idChat, json.dumps(chatData))
                    msg_send = "Pretende mudar de categoria de '" + chatData["cat"] + "' para '" + cat + "'? Responda por favor 'sim' ou 'não'"
            else:
                msg_send = process_params(idChat, idUser, msg, name, chatData)

    return str(msg_send)
