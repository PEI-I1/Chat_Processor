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
    ''' Cria um dic 'noccur' com o número de occorências na frase para cada categoria'''
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

# devolve uma string com o texto correto para pedir ao user a param_key
def pretty_print_param_key(param_key):
    param_key_string = ""

    if param_key == 'top':
        param_key_string =  "Deseja filtrar apenas os telemóveis mais procurados?"
    elif param_key == 'new':
        param_key_string =  "Deseja filtrar apenas os telemóveis mais recentes?"
    elif param_key == 'promo':
        param_key_string =  "Deseja filtrar apenas os telemóveis com promoção?"
    elif param_key == 'ofer':
        param_key_string =  "Deseja filtrar apenas os telemóveis que trazem ofertas?"
    elif param_key == 'prest':
        param_key_string =  "Deseja filtrar apenas os telemóveis que se podem pagar com prestações?"
    elif param_key == 'points':
        param_key_string =  "Deseja filtrar apenas os telemóveis que se podem pagar com pontos?"
    elif param_key == 'brand':
        param_key_string =  "Deseja filtrar por marca? Se sim indique qual, caso contrário responda 'não'"
    elif param_key == 'min':
        param_key_string =  "Por favor, introduza um valor mínimo para filtrar por preço. Caso não queira, responda 'não'."
    elif param_key == 'max':
        param_key_string =  "Por favor, introduza um valor máximo para filtrar por preço. Caso não queira, responda 'não'."
    elif param_key == 'assunto':
        param_key_string =  "Por favor indique qual linha de apoio que quer. Caso não saiba, responda 'não' para ver todas as opções."
    elif param_key == 'nome':
        param_key_string = "Por favor indique qual o nome do tarifário que deseja. Caso não saiba, responda 'não' para ver todas as opções."
    elif param_key == 'type':
        param_key_string = "Caso queira filtrar pelo tipo de pacote indique se quer 'Pacotes Fibra' ou 'Pacotes Satélite'. Caso não queira, responda 'não'."
    elif param_key == 'name':
        param_key_string = "Deseja filtrar pelo nome do pacote? Se sim indique qual, caso contrário responda 'não'."
    elif param_key == 'service':
        param_key_string = "Deseja filtrar por tipo de serviço do pacote? Se sim indique qual, caso contrário responda 'não'."

    return param_key_string

# adiciona elementos da new_list á old_list (chatData) se eles ainda nao existirem
def add_new_params(old_list, new_list):
    for (k,v) in new_list.items():
        if not k in old_list:
            old_list.update({k:v})

# quando um pedido é detetado, é feito o primeiro reconhecimento dos params
# e retorna-se a lista de parametros (obrigatorios/opcionais) (obtidos/em falta)
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
            print("[LOG] Valid required "+str(chatData['paramsRequired']))
            print("[LOG] Valid optional "+str(chatData['paramsOptional']))
            # altera status e guarda (se faltam params pergunta logo um deles)
            if len(missing_required_params) or len(missing_optional_params):
                chatData["paramsStatus"] = "missing"
                chatData["paramsMissingRequired"] = missing_required_params
                chatData["paramsMissingOptional"] = missing_optional_params
                globals.redis_db.set(idChat, json.dumps(chatData))
                print("[LOG] Missing required "+str(chatData['paramsMissingRequired']))
                print("[LOG] Missing optional "+str(chatData['paramsMissingOptional']))
                if len(missing_required_params):
                    param_key, param_value = list(missing_required_params.items())[0]
                    msg = "Precisamos de informação sobre:\n"+param_value
                elif len(missing_optional_params):
                    param_key, param_value = list(missing_optional_params.items())[0]

                    print("[LOG] " + param_key)
                    msg = pretty_print_param_key(param_key)

                    if not msg:
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
                first_key, first_value = list(chatData["paramsMissingOptional"].items())[0]
                # first_value = chatData["paramsMissingOptional"][first_key] # TODO: remove
                # FIXME: usar entidade detetada (no msg_params) em vez da msg diretamente
                # remover do missing o que foi detetado
                if 'nao' not in msg:
                    chatData["paramsOptional"][first_key] = msg
                del chatData["paramsMissingOptional"][first_key]
                globals.redis_db.set(idChat, json.dumps(chatData))

            print("[LOG] Valid required "+str(chatData['paramsRequired']))
            print("[LOG] Valid optional "+str(chatData['paramsOptional']))
            print("[LOG] Missing required "+str(chatData['paramsMissingRequired']))
            print("[LOG] Missing optional "+str(chatData['paramsMissingOptional']))
            if chatData["paramsMissingRequired"] == {} and chatData["paramsMissingOptional"] == {}:
                chatData["paramsStatus"] = "done"
            # perguntar params obrigatórios em falta
            else:
                if chatData["paramsMissingRequired"] != {}:
                    # FIXME: nao esta como devia, mas pelo menos tem mensagens personalizadas
                    #           e nunca se pedem muitos params
                    # send_msg(idChat, entry['missingRequiredParamsPhrase'])
                    param_key, param_value = list(chatData["paramsMissingRequired"].items())[0]
                    msg = "Precisamos de informação acerca de:\n"+param_value
                    send_msg(idChat, msg)
                elif chatData["paramsMissingOptional"] != {}:
                    param_key, param_value = list(chatData["paramsMissingOptional"].items())[0]
                    # TODO: traduzir o termo (param_key) para PT
                    # msg = "Pode-nos dizer algo acerca de:\n"+param_key+"\n(Responda 'nao' caso nao saiba)"
                    print("[LOG] " + param_key)
                    msg = pretty_print_param_key(str(param_key))

                    if msg is "":
                        msg = "Pode-nos dizer algo sobre:\n"+param_key+"\n(Responda 'nao' caso nao saiba)"
                    send_msg(idChat, msg)

        if chatData["paramsStatus"] == "done":
            print("[DEBUG] all done. sending response")
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
