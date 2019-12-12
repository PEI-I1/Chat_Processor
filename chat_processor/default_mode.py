from categoria_dic import cat as dicionario
from spell_checker import spell_check_ss
from utils import *
import globals, nltk, json, copy
import regex as re
from pretty_print import pretty_print

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
                if word == clean_msg(pal):
                    noccur[cat['request']] = noccur.get(cat['request'], 0) + 1
    return noccur

# com base na dic do noccur calcular qual é a categoria mais provável e a sua confiança
# confiança = noccur da categoria que aparece mais / número de ocorrência de todas as categorias
def calcula_confianca(noccur):
    if len(noccur):
        total = sum(noccur.values())
        cat_maior = max(noccur, key=noccur.get)
        confianca = noccur.get(cat_maior) / total
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

# lista os params opcionais que faltam
def lista_params_opcionais(missing_optional_params):
    lista = []
    frase = []
    resposta = []

    for (k,v) in missing_optional_params.items():
        if k is 'date':
            lista.append('data')
        elif k is 'start_time':
            lista.append('hora de início')
        elif k is 'end_time':
            lista.append('hora de fim')
        elif k is 'time':
            lista.append('duração')
        elif k is 'genre':
            lista.append('gênero')
        elif k is 'cast':
            lista.append('elenco')
        elif k is 'producer':
            lista.append('realizador')
        elif k is 'synopsis':
            lista.append('sinopse')
        elif k is 'age':
            lista.append('idade')
        else:
            if v['type'] is 'SUBJECT':
                lista.append('assunto')

    for i in range(0,len(lista)):
        if i < len(lista)-2:
            palavra = lista[i] + ', '
        elif i == len(lista)-2:
            palavra = lista[i] + ' e '
        else:
            palavra = lista[i] + '.'
        frase.append(palavra)

    frase = ''.join(frase)
    resposta = "Por favor, diga informações acerca de um destes parâmetros para adicionar à pesquisa: " + frase
    return resposta

# recolhe os params necessarios (params) apartir da DB (db_params) e da frase (msg_params)
def compare_params(params, msg_params, db_params):
    required_params = copy.deepcopy(db_params)
    size = len(msg_params)

    for (n, t) in params.items():
        if required_params.get(n,None) == None:
            found = None
            i = 0

            while i < size and found == None:
                if msg_params[i]["type"] == t:
                    found = {n:{"type":t,"entity":msg_params[i]["entity"]}}
                i+=1

            if found == None:
                found = {n:{"type":t}}

            required_params.update(found)

    return required_params

# devolve os params válidos e os params em falta
def separate_params(params):
    valid_params = {}
    missing_params = {}

    for (n,value) in params.items():
        # se tiver entity está validado, senao esta em falta
        if "entity" in value:
            valid_params[n] = value
        else:
            missing_params[n] = value

    return valid_params, missing_params

def add_new_params(l, new_l):
    for (k,v) in new_l.items():
        if not k in l:
            l.update({k:v})

# converte a estrutura dos parametros para a forma aceite pelo get_content
def convert_valid_params(valid_required_params,valid_optional_params):
    valid_required_params_array = []
    valid_optional_params_dict = {}

    for (n,value) in valid_required_params.items():
        valid_required_params_array[n] = value["entity"]
    for (n,value) in valid_optional_params.items():
        valid_optional_params_dict[n] = value["entity"]

    return valid_required_params_array, valid_optional_params_dict

def validAndMissingParams(msg_params, chatData, entry):
    # obrigatórios
    required_params = compare_params(entry['paramsRequired'], msg_params, chatData['paramsRequired'])
    valid_required_params, missing_required_params = separate_params(required_params)
    # opcionais
    optional_params = compare_params(entry['paramsOptional'], msg_params, chatData['paramsOptional'])
    valid_optional_params, missing_optional_params = separate_params(optional_params)

    return valid_required_params, missing_required_params, valid_optional_params, missing_optional_params

def convert_params_CC(msg_params, entry):
    # obrigatórios
    required_params = compare_params(entry['paramsRequired'], msg_params, {})
    valid_required_params, missing_required_params = separate_params(required_params)
    # opcionais
    optional_params = compare_params(entry['paramsOptional'], msg_params, {})
    valid_optional_params, missing_optional_params = separate_params(optional_params)

    return valid_required_params, valid_optional_params

def get_city(entry, msg_params):
    loc = None

    for p in msg_params:
        if p['type'] == entry['locationParam']['search_term']:
            loc = p['entity']

    return loc

def process_content(idChat, chatData, content):
    if content != None:
        if content:
            #se for uma lista devolve de forma diferente
            if isinstance(content, list):
                pretty_print(idChat, chatData["cat"], content, False)
                globals.redis_db.set("vermais" + str(idChat), json.dumps({"cat": chatData["cat"], "content": content}))
            else:
                pretty_print(idChat, chatData["cat"], content, True)
        else:
            send_msg(idChat, "Não existe informação sobre o que pretende...")
    else:
        send_msg(idChat, "Não foi possível obter a resposta...")

def process_params(idChat, idUser, msg, name, chatData, msg_params):
    detected_request = chatData["cat"]
    entry = get_entry(detected_request)
    location_params = entry['locationParam']
    needAtLeastOneOptionalParam = entry['needAtLeastOneOptionalParam']

    # quanto o pedido nao recebe params > devolve resposta
    if not entry['paramsRequired'] and not entry['paramsOptional'] and not location_params:
        process_content(idChat, chatData, get_content(detected_request, [], {}))
        globals.redis_db.delete(idChat)
    elif len(location_params) > 0 and chatData["locationParam"] == None and chatData["status"] != "gps_loc" and chatData["status"] != "search_loc":
        loc = get_city(entry, msg_params)

        if loc:
            chatData["locationParam"] = {"search_term": loc}
            chatData["status"] = ""
            process_params(idChat, idUser, msg, name, chatData, msg_params)
        else:
            chatData["status"] = "gps_loc"
            globals.redis_db.set(idChat, json.dumps(chatData))
            # pede ao utilizador a localização
            get_loc(idChat)
            send_msg(idChat, "Qual a sua localização?")
    elif chatData["status"] == "gps_loc":
        loc = get_city(entry, msg_params)

        if loc:
            chatData["locationParam"] = {"search_term": loc}
            chatData["status"] = ""
            process_params(idChat, idUser, msg, name, chatData, msg_params)
        else:
            chatData["status"] = "search_loc"
            globals.redis_db.set(idChat, json.dumps(chatData))
            send_msg(idChat, "Em que cidade se encontra?")
    elif chatData["status"] == "search_loc":
        loc = get_city(entry, msg_params)

        if loc:
            chatData["locationParam"] = {"search_term": loc}
            chatData["status"] = ""
            process_params(idChat, idUser, msg, name, chatData, msg_params)
        else:
            send_msg(idChat, "Não foi possível perceber onde se encontra!")
            globals.redis_db.delete(idChat)
    else:
        valid_required_params, missing_required_params, valid_optional_params, missing_optional_params = validAndMissingParams(msg_params, chatData, entry)
        # converter
        valid_required_params_array, valid_optional_params_dict = convert_valid_params(valid_required_params,valid_optional_params)
        # adicionar bd
        add_new_params(chatData['paramsRequired'], valid_required_params)
        add_new_params(chatData['paramsOptional'], valid_optional_params)
        print(valid_required_params)
        print(valid_optional_params)
        print(missing_required_params)
        print(missing_optional_params)

        # quando falta params obrigatório
        #   -> perguntar ao utilizador os parametros que faltam
        if len(missing_required_params):
            # FIXME: funciona para todos os nossos casos (só há um caso com 2params obrigatorios)
            #           pode ser melhorada qd coisas mais importantes estiverem resolvidas
            send_msg(idChat, entry['missingRequiredParamsPhrase'])
            globals.redis_db.set(idChat, json.dumps(chatData))
        # se faltarem params optionais
        elif len(missing_optional_params):
            # se precisarmos de um param optional e não existir nenhum (/scrapper/movies/search')
            if len(valid_optional_params) == 0 and needAtLeastOneOptionalParam is True:
                # FIXME: funciona para o unico caso que temos
                #         pode ser melhorada mais tarde
                send_msg(idChat, "Por favor, diga informações acerda de um destes parãmetros para fazer a pesquisa: gênero, elenco, realizador, sinopse ou idade")
                globals.redis_db.set(idChat, json.dumps(chatData))
            else:
                # processar resposta do user e devolver o conteudo pedido
                if chatData["status"] == "waitingMoreOptionalParams":
                    if clean_msg(msg) == "nao":
                        pass
                    else:
                        pass
                    # NOTE: acho que o if else é inutil really...
                    #       se nao houver params eles nao sao processados e nao
                    querystrings = merge_dicts(valid_optional_params_dict, chatData['locationParam'])
                    process_content(idChat, chatData, get_content(detected_request, valid_required_params_array, querystrings))
                    globals.redis_db.delete(idChat)
                # listar todos os params opcionais e esperar resposta
                else:
                  chatData["status"] = "waitingMoreOptionalParams"
                  globals.redis_db.set(idChat, json.dumps(chatData))
                  process_content(idChat, chatData, lista_params_opcionais(missing_optional_params))
        else: # nao faltam params opcionais
            querystrings = merge_dicts(valid_optional_params_dict, chatData['locationParam'])
            process_content(idChat, chatData, get_content(detected_request, valid_required_params_array, querystrings))
            globals.redis_db.delete(idChat)

def get_response_default(idChat, idUser, msg, name, chatData):
    #Mudar categoria???
    if chatData["status"] == "mudar categoria?":
        mc = clean_msg(msg)

        if mc == "sim":
            chatData["cat"] = chatData["cat_change"]

        entry = get_entry(chatData["cat"])
        valid_req_params, valid_opt_params = convert_params_CC(chatData["paramsRequired"], entry)
        chatData['paramsRequired'] = valid_req_params
        chatData['paramsOptional'] = valid_opt_params

        chatData["status"] == ""
        chatData["cat_change"] = ""

        params = proc_ents(globals.ner_model([msg]))
        process_params(idChat, idUser, msg, name, chatData, params)
    else:
        cat, confianca = get_categoria_frase(msg)
        print(cat)
        print(confianca)
        if msg != "":
            params = proc_ents(globals.ner_model([msg]))
        else:
            params = []

        if chatData["cat"] == "":
            if confianca > confianca_level:
                chatData["cat"] = cat
                globals.redis_db.set(idChat, json.dumps(chatData))
                process_params(idChat, idUser, msg, name, chatData, params)
            else:
                if chatData["tries"] == tries - 1:
                    send_msg(idChat, "Desculpe mas não foi possível identificar o que pretende.")
                    send_msg(idChat, "Pode tentar o modo de regras ao escrever 'modo de regras'.")
                    send_msg(idChat, "Ou pode se quiser ligar para uma das seguintes linhas de apoio:")
                    #TODO: tentar melhorar as linhas de apoio por forma a tentar mostrar apenas o de um assunto
                    linhas_apoio = get_content("/fs_scrapper/linhas_apoio", [], {})
                    if linhas_apoio:
                        pretty_print(idChat, "/fs_scrapper/linhas_apoio", linhas_apoio, True)
                    else:
                        send_msg(idChat, "Não foi possível obter as linhas de apoio...")
                    globals.redis_db.delete(idChat)
                else:
                    chatData["tries"] += 1
                    globals.redis_db.set(idChat, json.dumps(chatData))
                    send_msg(idChat, "Desculpe mas não foi possível identificar o que pretende. Tente de novo!")
        else:
            if confianca > confianca_level:
                if chatData["cat"] == cat:
                    process_params(idChat, idUser, msg, name, chatData, params)
                else:
                    chatData["cat_change"] = cat
                    chatData["paramsRequired"] = params
                    chatData["status"] = "mudar categoria?"
                    globals.redis_db.set(idChat, json.dumps(chatData))
                    #TODO: em vez da cat (path) aparecer um texto da cat
                    send_msg(idChat, "Pretende mudar de categoria de '" + chatData["cat"] + "' para '" + cat + "'? Responda por favor 'sim' ou 'não'")
            else:
                process_params(idChat, idUser, msg, name, chatData, params)
