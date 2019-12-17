from categoria_dic import cat as dicionario
from spell_checker import spell_check_ss
from utils import *
import globals, nltk, json, copy
import regex as re
from pretty_print import pretty_print
from ner_by_regex import detect_entities_regex

confianca_level = 0.70
tries = 5


def limpa_texto(mensagem):
    ''' Remove stopwords and punctuation from the input message
    :param: message to be cleaned
    :return: message after processing
    '''
    mensagem = nltk.word_tokenize(mensagem.lower())
    mensagem = ' '.join([clean_msg(palavra) for palavra in mensagem if not re.match('\p{punct}', palavra)])
    return mensagem


def criar_noccur_dic(frase):
    ''' Cria um dic 'noccur' com o número de occorências na frase para cada categoria
    '''
    noccur = {}
    for cat in dicionario:
        for expr,mod in cat['words']:
            if re.search(expr, frase):
                noccur[cat['request']] = noccur.get(cat['request'], 0) + mod
    return noccur

# com base na dic do noccur calcular qual é a categoria mais provável e a sua confiança
# confiança = noccur da categoria que aparece mais / número de ocorrência de todas as categorias
def calcula_confianca(noccur):
    if len(noccur):
        #total = sum(noccur.values())
        cat_maior = max(noccur, key=noccur.get)
        confianca = noccur.get(cat_maior) #/ total
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
        elif v['type'] is 'SUBJECT':
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

def detect_new_params(msg_params, entry):
    size = len(msg_params)

    required_params = {}
    required_missing_params = {}
    for (key, ent_type) in entry["paramsRequired"].items():
        i = 0
        found = None
        while i < size and found == None:
            if msg_params[i]["type"] == ent_type:
                found = {key:msg_params[i]["entity"]}
            i += 1
        if found:
            required_params.update(found)
        else:
            required_missing_params.update({key:ent_type})

    optional_params = {}
    optional_missing_params = {}
    for (key, ent_type) in entry["paramsOptional"].items():
        i = 0
        found = None
        while i < size and found == None:
            if msg_params[i]["type"] == ent_type:
                found = {key:msg_params[i]["entity"]}
            i += 1
        if found:
            optional_params.update(found)
        else:
            optional_missing_params.update({key:ent_type})

    return required_params, required_missing_params, optional_params, optional_missing_params

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

    if '|' in entry['locationParam']['search_term']:
        types = entry['locationParam']['search_term'].split('|')
    else:
        types = [entry['locationParam']['search_term']]

    for p in msg_params:
        for t in types:
            if p['type'] == t:
                loc = p['entity']

    return loc

def process_content(idChat, chatData, content):
    if content != None:
        if content:
            #se for uma lista devolve de forma diferente
            if isinstance(content, list) and len(content) > 5:
                pretty_print(idChat, chatData["cat"], content[:5], False)
                globals.redis_db.set("vermais" + str(idChat), json.dumps({"cat": chatData["cat"], "content": content[5:]}))
            else:
                pretty_print(idChat, chatData["cat"], content, True)
        else:
            send_msg(idChat, "Não existe informação sobre o que pretende...")
    else:
        send_msg(idChat, "Não foi possível obter a resposta...")

def detect_params(msg):
    #detect entities using deepavlov NER model
    params = proc_ents(globals.ner_model([msg]))
    #detect entities using regex
    params = params + detect_entities_regex(msg)
    #remove duplicates
    params = list({json.dumps(p):p for p in params}.values())
    return params

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
        # new problem. save obtained params
        if chatData["paramsStatus"] == "new":
            # process msg params, save
            required_params, missing_required_params, optional_params, missing_optional_params = detect_new_params(msg_params, entry)
            # TODO: tratar do caso em que é preciso pelo menos um params
            # needAtLeastOneOptionalParam = entry['needAtLeastOneOptionalParam']
            # adicionar ao redis
            add_new_params(chatData['paramsRequired'], required_params)
            add_new_params(chatData['paramsOptional'], optional_params)
            print("[LOG] Valid required "+str(required_params))
            print("[LOG] Valid optional "+str(optional_params))
            # altera status e guarda (se faltam params pergunta logo um deles)
            if len(missing_required_params) or len(missing_optional_params):
                chatData["paramsStatus"] = "missing"
                chatData["paramsMissingRequired"] = missing_required_params
                chatData["paramsMissingOptional"] = missing_optional_params
                globals.redis_db.set(idChat, json.dumps(chatData))
                print("[LOG] Missing required "+str(missing_required_params))
                print("[LOG] Missing optional "+str(missing_optional_params))
                if len(missing_required_params):
                    param_key, param_value = list(missing_required_params.items())[0]
                    msg = "Precisamos de informação sobre:\n"+param_value
                elif len(missing_optional_params):
                    param_key, param_value = list(missing_optional_params.items())[0]
                    msg = "Pode-nos dizer algo sobre:\n"+param_key+"\n(Responda 'nao' caso nao saiba)"
                send_msg(idChat, msg)
            else:
                chatData["paramsStatus"] = "done"
        elif chatData["paramsStatus"] == "missing":
            print("[DEBUG] adding param given by user")
            # save param given by user
            if len(chatData["paramsMissingRequired"]):
                first_key, first_value = list(chatData["paramsMissingRequired"].items())[0]
                # first_value = chatData["paramsMissingRequired"][first_key] # TODO: remove
                # FIXME: usar entidade detetada (no msg_params) em vez da msg diretamente
                # remover do missing o que foi detetado
                chatData["paramsRequired"][first_key] = msg
                del chatData["paramsMissingRequired"][first_key]
                globals.redis_db.set(idChat, json.dumps(chatData))
            elif len(chatData["paramsMissingOptional"]):
                print(chatData["paramsMissingOptional"])
                first_key, first_value = list(chatData["paramsMissingOptional"].items())[0]
                # first_value = chatData["paramsMissingOptional"][first_key] # TODO: remove
                # FIXME: usar entidade detetada (no msg_params) em vez da msg diretamente
                # remover do missing o que foi detetado
                chatData["paramsOptional"][first_key] = msg
                del chatData["paramsMissingOptional"][first_key]
                globals.redis_db.set(idChat, json.dumps(chatData))

            if chatData["paramsMissingRequired"] == {} and chatData["paramsMissingOptional"] == {}:
                chatData["paramsStatus"] = "done"
            # perguntar params obrigatórios em falta
            else:
                if chatData["paramsMissingRequired"] != {}:
                    # FIXME: nao esta como devia, mas pelo menos tem mensagens personalizadas
                    #           e nunca se pedem muitos params
                    # send_msg(idChat, entry['missingRequiredParamsPhrase'])
                    param_key, param_value = list(missing_required_params.items())[0]
                    msg = "Precisamos de informação acerca de:\n"+param_value
                    send_msg(idChat, msg)
                elif chatData["paramsMissingOptional"] != {}:
                    param_key, param_value = list(missing_optional_params.items())[0]
                    # TODO: traduzir o termo (param_key) para PT
                    msg = "Pode-nos dizer algo acerca de:\n"+param_key+"\n(Responda 'nao' caso nao saiba)"
                    send_msg(idChat, msg)

        if chatData["paramsStatus"] == "done":
            print("[DEBUG] all done. sending response")
            # valid_required_params_array, valid_optional_params_dict = convert_valid_params(chatData["paramsRequired"],chatData["paramsOptional"])
            querystrings = merge_dicts(chatData["paramsOptional"], chatData['locationParam'])
            process_content(idChat, chatData, get_content(detected_request, chatData["paramsRequired"], querystrings))
            globals.redis_db.delete(idChat)

def get_response_default(idChat, idUser, msg, name, chatData):
    #Mudar categoria???
    if chatData["status"] == "mudar categoria?":
        mc = clean_msg(msg)

        if mc == "sim":
            chatData["cat"] = chatData["cat_change"]

        entry = get_entry(chatData["cat"])
        # valid_req_params, valid_opt_params = convert_params_CC(chatData["paramsRequired"], entry)
        # chatData['paramsRequired'] = valid_req_params
        # chatData['paramsOptional'] = valid_opt_params

        chatData["status"] == ""
        chatData["cat_change"] = ""

        params = detect_params(msg)
        process_params(idChat, idUser, msg, name, chatData, params)
    else:
        cat, confianca = get_categoria_frase(msg)
        print(cat)
        print(confianca)
        if msg != "":
            params = detect_params(msg)
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
