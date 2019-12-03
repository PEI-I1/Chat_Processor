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

    for i in range(0,len(lista)):
        if i < len(lista)-2:
            palavra = lista[i] + ', '
        elif i == len(lista)-2:
            palavra = lista[i] + ' e '
        else:
            palavra = lista[i] + '.'
        frase.append(palavra)

    frase = ''.join(frase)
    resposta = "Por favor, diga informações acerda de um destes parãmetros para adicionar à pesquisa: " + frase
    return resposta

# recolhe os params necessarios (params) apartir da DB (db_params) e da frase (msg_params)
def compare_params(params, msg_params, db_params):
    required_params = {}
    required_params.update(db_params)

    for (n, t) in params.items():
        if not required_params.get(n,None):
            found = None
            for pp in msg_params:
                if pp.type == t:
                    found = {n:{"type":t,"entity":pp.entity}}

            if not found:
                found = {n:{"type":t}}

            required_params.update(found)

    return required_params

# devolve os params válidados e os params em falta
def separate_params(params):
    valid_params = {}
    missing_params = {}

    for (n,value) in params.items():
        # se tiver entity está validado, senao esta em falta
        if value.get('entity', None):
            valid_params.update({n:value})
        else:
            missing_params.update({n:value})

    return valid_params, missing_params

def add_new_params(l, new_l):
    for p in new_l:
        if len([param for param in l if param == p]) == 0:
            l.append(p)

# converte a estrutura dos parametros para a forma aceite pelo get_content
def convert_valid_params(valid_required_params,valid_optional_params):
    valid_required_params_array = []
    valid_optional_params_array = {}

    for (n,value) in valid_required_params.items():
        valid_required_params_array[n] = value.entity
    for (n,value) in valid_optional_params.items():
        valid_required_params_array.update({n: value.entity})

    return valid_required_params_array, valid_optional_params_array

def process_params(idChat, idUser, msg, name, chatData):
    detected_request = chatData["cat"]
    entry = get_entry(detected_request)
    paramsRequired = entry['paramsRequired']
    paramsOptional = entry['paramsOptional']
    location_params = entry['locationParam']
    needAtLeastOneOptionalParam = entry['needAtLeastOneOptionalParam']
    msg_params = proc_ents(globals.ner_model([msg]))
    content = None

    # quanto o pedido nao recebe params > devolve resposta
    if not paramsRequired and not paramsOptional and not location_params:
        content = get_content(detected_request, [], {})
        globals.redis_db.delete(idChat)
        pass
    else:
        # obrigatórios
        required_params = compare_params(paramsRequired, msg_params, chatData['paramsRequired'])
        valid_required_params, missing_required_params = separate_params(required_params)
        # opcionais
        optional_params = compare_params(paramsOptional, msg_params, chatData['paramsOptional'])
        valid_optional_params, missing_optional_params = separate_params(paramsOptional)
        # converter
        valid_required_params_array, valid_required_params_array = convert_valid_params(valid_required_params,valid_optional_params)
        # adicionar bd
        add_new_params(chatData['paramsRequired'], valid_required_params)
        add_new_params(chatData['paramsOptional'], valid_optional_params)
        globals.redis_db.set(idChat, json.dumps(chatData))

        # quando falta params obrigatório
        #   -> perguntar ao utilizador os parametros que faltam
        if len(missing_required_params):
            # FIXME: funciona para todos os nossos casos (só há um caso com 2params obrigatorios)
            #           pode ser melhorada qd coisas mais importantes estiverem resolvidas
            return entry['missingRequiredParamsPhrase']

        # se faltarem params optionais
        if len(missing_optional_params):
            # se precisarmos de um param optional e não existir nenhum (/scrapper/movies/search')
            if len(valid_optional_params) == 0 and needAtLeastOneOptionalParam is True:
                # FIXME: funciona para o unico caso que temos
                #         pode ser melhorada mais tarde
                resposta = "Por favor, diga informações acerda de um destes parãmetros para fazer a pesquisa: gênero, elenco, realizador, sinopse ou idade"
                return resposta
            else:
                # processar resposta do user e devolver o conteudo pedido
                if chatData["status"] == "waitingMoreOptionalParams":
                    # FIXME: dar mais opçoes de negaçao para o user
                    if "nao" in msg:
                        pass
                    else:
                        pass
                    # NOTE: acho que o if else é inutil really...
                    #       se nao houver params eles nao sao processados e nao
                    content = get_content(detected_request, valid_required_params_array, valid_required_params_array)
                    globals.redis_db.delete(idChat)
                # listar todos os params opcionais e esperar resposta
                else:
                  chatData["status"] = "waitingMoreOptionalParams"
                  globals.redis_db.set(idChat, json.dumps(chatData))
                  resposta = lista_params_opcionais(missing_optional_params)
                  return resposta
        else: # nao faltam params opcionais
            content = get_content(detected_request, valid_required_params_array, valid_required_params_array)
            globals.redis_db.delete(idChat)

    if content:
        #se for uma lista devolve de forma diferente
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

