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


# devolve uma string com a questao apropriada para pedir ao user um param obrigatorio (param_key)
def pretty_question_required_param(param_key):
    pretty_response = ""

    if param_key == 'movie':
        pretty_response =  "Por favor, indique o filme que procura."
    elif param_key == 'duration':
        pretty_response =  "Por favor, indique a duração que pretende."
    else: # caso a key nao exista (nao é uma boa questão, mas melhor que nada)
        pretty_response = "Pedimos desculpa, mas poderia-nos dizer algo sobre: "+param_key

    return pretty_response

# devolve uma string com a questao apropriada para pedir ao user um param opcional (param_key)
def pretty_question_optional_param(param_key):
    pretty_response = ""

    # FS_scrapper params
    if param_key == 'top':
        pretty_response =  "Deseja filtrar apenas os telemóveis mais procurados?"
    elif param_key == 'new':
        pretty_response =  "Deseja filtrar apenas os telemóveis mais recentes?"
    elif param_key == 'promo':
        pretty_response =  "Deseja filtrar apenas os telemóveis com promoção?"
    elif param_key == 'ofer':
        pretty_response =  "Deseja filtrar apenas os telemóveis que trazem ofertas?"
    elif param_key == 'prest':
        pretty_response =  "Deseja filtrar apenas os telemóveis que se podem pagar com prestações?"
    elif param_key == 'points':
        pretty_response =  "Deseja filtrar apenas os telemóveis que se podem pagar com pontos?"
    elif param_key == 'brand':
        pretty_response =  "Deseja filtrar por marca? Se sim indique qual, caso contrário responda 'não'"
    elif param_key == 'min':
        pretty_response =  "Por favor, introduza um valor mínimo para filtrar por preço. Caso não queira, responda 'não'."
    elif param_key == 'max':
        pretty_response =  "Por favor, introduza um valor máximo para filtrar por preço. Caso não queira, responda 'não'."
    elif param_key == 'assunto':
        pretty_response =  "Por favor indique qual linha de apoio que quer. Caso não saiba, responda 'não' para ver todas as opções."
    elif param_key == 'nome':
        pretty_response = "Por favor indique qual o nome do tarifário que deseja. Caso não saiba, responda 'não' para ver todas as opções."
    elif param_key == 'type':
        pretty_response = "Caso queira filtrar pelo tipo de pacote indique se quer 'Pacotes Fibra' ou 'Pacotes Satélite'. Caso não queira, responda 'não'."
    elif param_key == 'name':
        pretty_response = "Deseja filtrar pelo nome do pacote? Se sim indique qual, caso contrário responda 'não'."
    elif param_key == 'service':
        pretty_response = "Deseja filtrar por tipo de serviço do pacote? Se sim indique qual, caso contrário responda 'não'."
    # Cinemas params
    elif param_key == 'genre':
        pretty_response = "Deseja filtrar pelo género? Se sim indique qual, caso contrário responda 'não'."
    elif param_key == 'cast':
        pretty_response = "Deseja filtrar pelo elenco? Se sim indique os atores procura, caso contrário responda 'não'."
    elif param_key == 'producer':
        pretty_response = "Deseja filtrar pelo produtor? Se sim indique qual, caso contrário responda 'não'."
    elif param_key == 'synopsis':
        pretty_response = "Deseja filtrar pela sinopse? Se sim diga parte da sinopse, caso contrário responda 'não'."
    elif param_key == 'age':
        pretty_response = "Deseja filtrar pela restrição de idade? Se sim indique qual, caso contrário responda 'não'."
    elif param_key == 'date':
        pretty_response = "Deseja filtrar por data? Se sim indique qual, caso contrário responda 'não'."
    elif param_key == 'start_time':
        pretty_response = "Deseja filtrar por hora de inicio? Se sim indique qual, caso contrário responda 'não'."
    elif param_key == 'end_time':
        pretty_response = "Deseja filtrar por hora de fim? Se sim indique qual, caso contrário responda 'não'."
     # caso a key nao exista (nao é uma boa questão, mas melhor que nada)
    else:
        pretty_response = "Pode-nos dizer algo sobre: "+param_key+"\n(Responda 'nao' caso nao saiba)"

    return pretty_response

# traduz um param em ingles para PT, para poder ser introduzido em mensagens
def localizeToPT(param):
    param_pt = ""

    if param == 'genre':
        param_pt =  "género"
    elif param == 'cast':
        param_pt =  "elenco"
    elif param == 'producer':
        param_pt =  "produtor"
    elif param == 'synopsis':
        param_pt =  "sinopse"
    elif param == 'age':
        param_pt =  "restrição de idade"
    # TODO: fazer para params do FS_scraper
    else: # caso a key nao exista (nao traduz, mas avisa)
        param_pt = param+" (pedimos desculpa pelo inglês)"

    return param_pt

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
                # TODO: falta outro if para tratar do caso de intervalos de tempo/dinheiro
                # if para separar os varios para diferentes PHONES_BOOLEAN
                if msg_params[i]["type"] == "PHONES_BOOLEAN":
                    if msg_params[i]["entity"] == key:
                        # found = {key:msg_params[i]["entity"]}
                        found = {key:"yes"}
                else:
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

def modo_problemas(idChat, msg, chatData):
    chatData["status"] = "modo problemas"
    globals.redis_db.set(idChat, json.dumps(chatData))
    send_msg(idChat, get_solver(idChat, msg))

def process_params(idChat, idUser, msg, name, chatData, msg_params):
    detected_request = chatData["cat"]
    entry = get_entry(detected_request)
    location_params = entry['locationParam']

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
            # adicionar ao redis
            add_new_params(chatData['paramsRequired'], required_params)
            add_new_params(chatData['paramsOptional'], optional_params)
            print("[LOG] Valid required "+str(chatData['paramsRequired']))
            print("[LOG] Valid optional "+str(chatData['paramsOptional']))

            # se for preciso pelo menos um param, envia um aviso ao user (e diz já a lista de params que terá)
            if entry['needAtLeastOneOptionalParam'] and len(chatData['paramsOptional']) == 0:
                print("[LOG] NeedAtLeastOneParam !!! ")
                warning_msg = "Esta busca precisará no minimo de um destes campos:\n"
                for param in missing_optional_params:
                    warning_msg += '-> '+localizeToPT(param)+'\n'
                send_msg(idChat, warning_msg)

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
                    if isinstance(param_key, int):
                        print("[LOG] Asking Required param (param_value): " + param_value)
                        param = param_value
                    else:
                        print("[LOG] Asking Required param (param_key): " + param_key)
                        param = param_key
                    msg = pretty_question_required_param(param)
                elif len(missing_optional_params):
                    param_key, param_value = list(missing_optional_params.items())[0]
                    print("[LOG] Asking param_key: " + param_key)
                    msg = pretty_question_optional_param(param_key)
                send_msg(idChat, msg)
            else:
                chatData["paramsStatus"] = "done"
        # processing problem by asking and saving missing params
        elif chatData["paramsStatus"] == "missing":
            print("[DEBUG] adding param given by user")
            # save param given by user
            if len(chatData["paramsMissingRequired"]):
                first_key, first_value = list(chatData["paramsMissingRequired"].items())[0]
                # FIXME: usar entidade detetada (no msg_params) em vez da msg diretamente
                # remover do missing o que foi detetado
                chatData["paramsRequired"][first_key] = msg
                del chatData["paramsMissingRequired"][first_key]
                globals.redis_db.set(idChat, json.dumps(chatData))
            elif len(chatData["paramsMissingOptional"]):
                first_key, first_value = list(chatData["paramsMissingOptional"].items())[0]
                # FIXME: usar entidade detetada (no msg_params) em vez da msg diretamente
                # remover do missing o que foi detetado
                if 'nao' != clean_msg(msg):
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
                    param_key, param_value = list(chatData["paramsMissingRequired"].items())[0]
                    if isinstance(param_key, int):
                        print("[LOG] Asking Required param (param_value): " + param_value)
                        param = param_value
                    else:
                        print("[LOG] Asking Required param (param_key): " + param_key)
                        param = param_key
                    msg = pretty_question_required_param(param)
                elif chatData["paramsMissingOptional"] != {}:
                    param_key, param_value = list(chatData["paramsMissingOptional"].items())[0]
                    print("[LOG] Asking Optional param (param_key): " + param_key)
                    msg = pretty_question_optional_param(str(param_key))
                send_msg(idChat, msg)
        # devolve resposta (todos os params foram obtidos), ou retorna falha (qd necessario minimo um param)
        if chatData["paramsStatus"] == "done":
            if entry['needAtLeastOneOptionalParam'] and len(chatData['paramsOptional']) == 0:
                send_msg(idChat, "Pedimos desculpa, mas sem preencher nenhum dos campos não podemos efetuar a sua pesquisa :(")
            else:
                print("[LOG] All info collected. Sending response")
                querystrings_aux = merge_dicts(chatData["paramsOptional"], chatData['locationParam'])
                querystrings = merge_dicts(chatData["paramsRequired"], querystrings_aux)
                process_content(idChat, chatData, get_content(detected_request, [], querystrings))
            globals.redis_db.delete(idChat)

def get_response_default(idChat, idUser, msg, name, chatData):
    if chatData["status"] == "mudar categoria?":
        muda_categoria = clean_msg(msg)

        # se o user quiser mudar, altera-se a categoria e marca-se como new para os params
        if muda_categoria == "sim":
            chatData["cat"] = chatData["cat_change"]
            chatData["paramsStatus"] = "new"
        # se o user nao quiser mudar, trata-se a ultima mensagem (antes de perguntar se queria mudar de pedido)
        else:
            msg = chatData["cat_change_last_msg"]

        chatData["status"] = ""
        chatData["cat_change"] = ""
        chatData["cat_change_last_msg"] = ""

        if chatData["cat"] == "/solver":
            modo_problemas(idChat, msg, chatData)
        else:
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
                if cat == "/solver":
                    modo_problemas(idChat, msg, chatData)
                else:
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
                    chatData["cat_change_last_msg"] = msg
                    chatData["status"] = "mudar categoria?"
                    globals.redis_db.set(idChat, json.dumps(chatData))
                    #TODO: em vez da cat (path) aparecer um texto da cat
                    send_msg(idChat, "Pretende mudar de categoria de '" + chatData["cat"] + "' para '" + cat + "'? Responda por favor 'sim' ou 'não'")
            else:
                process_params(idChat, idUser, msg, name, chatData, params)
