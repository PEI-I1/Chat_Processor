from categoria_dic import cat as dicionario
from spell_checker import spell_check_ss
from utils import *
import globals, nltk, json, copy
import regex as re
from datetime import date, timedelta
from pretty_print import pretty_print
from ner_by_regex import detect_entities_regex
from pretty_params import optional_params as pp_opt, required_params as pp_req, param_en_to_pt
from text_to_number import parse_number
from config import PARAM_THRESHOLD
from prefab_msgs import prefab_msgs

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
    ''' Creates a dictionary 'noccur' with the number of ocurrences for each category/functionality in phrase
    :param: phrase
    :return: dictionary
    '''
    noccur = {}
    for cat in dicionario:
        for expr,mod in cat['words']:
            if re.search(expr, frase):
                noccur[cat['request']] = noccur.get(cat['request'], 0) + mod
    return noccur

def calcula_confianca(noccur):
    '''For a given noccur calculates the most likely category/functionality and its confidence
    :param: dictionary (noccur)
    :return: category/functionality and confidence
    '''
    if len(noccur):
        #total = sum(noccur.values())
        cat_maior = max(noccur, key=noccur.get)
        confianca = noccur.get(cat_maior) #/ total
    else:
        cat_maior = "Not Found"
        confianca = 0
    return cat_maior,confianca

def get_categoria_frase(inp):
    '''For a given user message obtains its category/functionality and confidence
    :param: user message
    :return: category/functionality and confidence
    '''
    inp = spell_check_ss(inp)
    palavras = limpa_texto(inp)
    noccur = criar_noccur_dic(palavras)
    return calcula_confianca(noccur)

def proc_ents(inp):
    '''For the given answer of deeppavlov model constructs an list with the entities
    in a appropriate structure
    :param: answer given by the deeeppavlov model
    :return: a list with the entities (value and type)
    '''
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

def pretty_question_required_param(param_key):
    '''For a given required param returns a string with the appropriate question
    :param: required parameter
    :return: string with question to user
    '''
    return pp_req.get(param_key, "Pedimos desculpa, mas poderia-nos dizer algo sobre: " + param_key)

def pretty_question_optional_param(param_key):
    '''For a given optional param returns a string with the appropriate question
    :param: optional parameter
    :return: string with question to user
    '''
    return pp_opt.get(param_key, prefab_msgs["request"][1].format(param_key))

def localizeToPT(param):
    '''Translate a parameter in english to portuguese in order to put in messages sended to user
    :param: parameter to translate
    :return: translated parameter
    '''
    return param_en_to_pt.get(param, prefab_msgs["misc"][0].format(param))

def add_new_params(old_list, new_list):
    '''Add elements of a source list to a destination list if element not exists in the destination list
    :param: destination list
    :param: source list
    :return: updated destination list'''
    for (k,v) in new_list.items():
        if not k in old_list:
            old_list.update({k:v})

def parse_date_time(string):
    '''Parses entities of type date and time in order to try detect some aditional ways of saying date or time
    and put them in a correct format to routes of scrapers
    :param: string with date/time to parse
    '''
    params = []
    td = date.today()
    cs = clean_msg(string)

    if re.search(r'\bamanha\b', cs):
        tm = td + timedelta(days=1)
        params.append({'date': tm.strftime('%Y-%m-%d')})
    elif re.search(r'\bhoje\b', clean_msg(string)):
        params.append({'date': td.strftime('%Y-%m-%d')})

    if re.search(r'\bmanha\b', cs):
        params.append({'start_time': '06:00:00'})
        params.append({'end_time': '12:00:00'})
    elif re.search(r'\btarde\b', cs):
        params.append({'start_time': '12:00:00'})
        params.append({'end_time': '20:00:00'})
    elif re.search(r'\bnoite\b', cs):
        params.append({'start_time': '20:00:00'})
        params.append({'end_time': '06:00:00'})

    return params

def parse_date(key, string):
    '''Parses entities of type date in order to put it in a correct format to routes of scrapers
    :param: string with date to parse
    '''
    params = parse_date_time(string)
    mounths = {
        'janeiro': '01',
        'fevereiro': '02',
        'marco': '03',
        'abril': '04',
        'maio': '05',
        'junho': '06',
        'julho': '07',
        'agosto': '08',
        'setembro': '09',
        'outubro': '10',
        'novembro': '11',
        'dezembro': '12'
    }

    st = '(' + '|'.join(mounths.keys()) + ')'

    if not len(params):
        string = parse_number(string)
        if re.match(r'^\s*entre\s+[0-9]+\s+e\s+[0-9]+\s*$', string):
            string = re.sub(r'^\s*entre\s+([0-9]+)\s+e\s+([0-9]+)\s*$', r'\1|\2', string)
            nums = string.split('|')
            if nums[0] == nums[1]:
                params.append({'min': nums[0]})
            elif float(nums[0]) < float(nums[1]):
                params.append({'min': nums[0]})
                params.append({'max': nums[1]})
            else:
                params.append({'min': nums[1]})
                params.append({'max': nums[0]})
        elif re.match(r'\s*[0-9]+\s*anos?\s*', string):
            string = re.sub(r'\s*([0-9]+)\s*anos?\s*', r'\1', string)
            params.append({'age': string})
        elif key != 'age':
            string = re.sub(r''+st, lambda x: mounths[x[0]], clean_msg(string))
            string = re.sub(r'[^0-9]+',r'-', string)

            string = re.sub(r'^([0-9])-', r'0\1-', string)
            string = re.sub(r'-([0-9])-', r'-0\1-', string)

            ss = string.split('-')
            ss = ss[::-1]
            string = '-'.join(ss)
            params.append({key: string})

    return params

def parse_time(key, string):
    '''Parses entities of type time in order to put it in a correct format to routes of scrapers
    :param: string with time to parse
    '''
    params = parse_date_time(string)

    if not len(params):
        string = parse_number(string)
        if re.match(r'^\s*[0-9]+\s*m(in(utos?)?)?\s*$', string):
            string = re.sub(r'^\s*([0-9]+)\s*m(in(utos?)?)?\s*$', r'\1', string)
            params.append({'duration': string})
        elif key != 'duration':
            string = re.sub(r'^([0-9]+)a?\s*h(oras?)?\s*$',r'\1:00',string)
            string = re.sub(r'^([0-9]+)\s*m(in(utos?)?)?\s*$',r'00:\1',string)
            string = re.sub(r'[^0-9]*([0-9]+)[^0-9]+([0-9]+)[^0-9]*', r'\1:\2:00', string)
            string = re.sub(r'^([0-9]):', r'0\1:', string)
            string = re.sub(r':([0-9]):', r':0\1:', string)
            string = re.sub(r'^\s*([0-9]+)\s*:\s*$', r'\1:00:00', string)
            string = re.sub(r'^\s*([0-9]+)\s*:\s*([0-9]+)\s*:?\s*$', r'\1:\2:00', string)
            params.append({key: string})

    return params

def parse_money_cardinal(key, string):
    '''Parses entities of type money/cardinal in order to put it in a correct format to routes of scrapers
    :param: string with money/cardinal to parse
    '''
    string = re.sub(r'\s*euros?\s*', '', string)
    string = re.sub(r'\s*€\s*', '', string)

    if re.match(r'^\s*entre\s+[0-9]+\s+e\s+[0-9]+\s*$', string):
        print(string)
        string = re.sub(r'^\s*entre\s+([0-9]+)\s+e\s+([0-9]+)\s*$', r'\1|\2', string)
        nums = string.split('|')
        if nums[0] == nums[1]:
            return [{'min': nums[0]}]
        elif float(nums[0]) < float(nums[1]):
            return [{'min': nums[0]}, {'max': nums[1]}]
        else:
            return [{'min': nums[1]}, {'max': nums[0]}]
    else:
        string = parse_number(string)
        return [{key: re.sub(r'\s+', '', string)}]

def compare_params(found, params, chatData, fst_key, sec_key):
    '''Compare parameters in order to discover whitch one is bigger and to put them in the correct order
    :param: parameters discovered with this detected entity
    :param: parameters discovered in this phrase at the moment
    :param: user chat state
    :param: parameter key with supposedly lower value
    :param: parameter key with supposedly bigger value
    '''
    valueS = None
    valueE = None
    indS = -1
    indE = -1

    if fst_key == 'min' and sec_key == 'max':
        func = float
    else:
        func = str

    for index, f in enumerate(found):
        k, v = list(f.items())[0]
        if k == fst_key:
            valueS = v
            indS = index
        if k == sec_key:
            valueE = v
            indE = index
    if indE != -1 and valueE != None:
        if fst_key in params:
            if params[fst_key] == valueE:
                del found[indE]
            elif func(params[fst_key]) > func(valueE):
                found[indE][sec_key] = params[fst_key]
                params[fst_key] = valueE
        elif fst_key in chatData['paramsOptional']:
            if chatData['paramsOptional'][fst_key] == valueE:
                del found[indE]
            elif func(chatData['paramsOptional'][fst_key]) > func(valueE):
                found[indE][sec_key] = chatData['paramsOptional'][fst_key]
                chatData['paramsOptional'][fst_key] = valueE
        elif indS != -1 and valueS != None:
            if valueS == valueE:
                del found[indE]
            elif func(valueS) > func(valueE):
                found[indS][fst_key] = valueE
                found[indE][sec_key] = valueS

def is_blacklisted(st):
    '''Check if string is not blacklisted
    :param: string to check
    '''
    blacklisted = False
    l = len(globals.blacklist)
    i = 0
    
    while i < l and not blacklisted:
        if re.match(globals.blacklist[i], st):
            blacklisted = True
        i += 1

    return blacklisted

def transform_param(key, msg_param, params, chatData):
    '''Transform a param
    :param: key of param
    :param: parameter
    '''
    found = []

    #check if is not in blacklist
    if not is_blacklisted(msg_param["entity"]):
        if "TIME" in msg_param["type"]:
            found = parse_time(key, msg_param["entity"])
            if key == 'end_time':
                compare_params(found, params, chatData, 'start_time', 'end_time')
        elif "DATE" in msg_param["type"]:
            found = parse_date(key, msg_param["entity"])
        elif "CARDINAL" in msg_param["type"]:
            found = parse_money_cardinal(key, msg_param["entity"])
            if key == 'max':
                compare_params(found, params, chatData, 'min', 'max')
        elif "MONEY" in msg_param["type"]:
            found = parse_money_cardinal(key, msg_param["entity"])
            if key == 'max':
                compare_params(found, params, chatData, 'min', 'max')
        elif "PHONES_BOOLEAN" in msg_param["type"]:
            if msg_param["entity"] == key:
                found = [{key:"yes"}]
        elif "PERSON" in msg_param["type"]:
            if key == "producer":
                if "cast" not in params or params["cast"] != msg_param["entity"]:
                    found = [{key:msg_param["entity"]}]
            else:
                found = [{key:msg_param["entity"]}]
        else:
            found = [{key:msg_param["entity"]}]

    return found

def new_params(entry_params, msg_params, size, chatData):
    ''' Auxiliar function for initial recognition of params, detects missing params
    :param: parameters of category
    :param: parameters detected in message
    :param: number of parameters detected in message
    :param: function to convert each parameter
    '''
    params = {}
    missing_params = {}

    for (key, ent_type_list) in entry_params.items():
        for ent_type in ent_type_list.split('|'):
            i = 0
            found = []

            while i < size and found == []:
                if msg_params[i]["type"] == ent_type:
                    found = transform_param(key, msg_params[i], params, chatData)
                i += 1

            for f in found:
                params.update(f)

        if key not in params:
            missing_params.update({key:ent_type_list})

    return params, missing_params

def detect_new_params(msg_params, entry, chatData):
    ''' Initial recognition of params, detects missing params
    :param: parameters detected in user message
    :param: entry in categoria_dict of category/functionality
    :return: detected required parameters, missing required parameters, detected optional parameters, missing optional parameters
    '''
    size = len(msg_params)
    required_params, required_missing_params = new_params(entry["paramsRequired"], msg_params, size, chatData)
    optional_params, optional_missing_params = new_params(entry["paramsOptional"], msg_params, size, chatData)
    return required_params, required_missing_params, optional_params, optional_missing_params

def get_city(entry, msg_params):
    ''' Obtain the detected parameters in user message that matches with search_term
    :param: entry in categoria_dict of category/functionality
    :param: parameters detected in user message
    :return: address or city that user sended in message
    '''
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
    '''Pretty print of content, sending messages to user and when content
    are lists only send first 5 elements
    :param: id chat
    :param: user chat state
    :param: content that will be send to user
    '''
    if content != None:
        if content:
            #se for uma lista devolve de forma diferente
            if isinstance(content, list) and len(content) > 5 and chatData["cat"] != '/fs_scrapper/linhas_apoio':
                pretty_print(idChat, chatData["cat"], content[:5], False)
                globals.redis_db.set("vermais" + str(idChat), json.dumps({"cat": chatData["cat"], "content": content[5:]}))
            else:
                pretty_print(idChat, chatData["cat"], content, True)
        else:
            send_msg(idChat, prefab_msgs["failed"][1])
    else:
        send_msg(idChat, prefab_msgs["failed"][2])

def detect_params(msg):
    '''Detect parameters(entities) in user message
    :param: user message
    :return: list with detected parameters
    '''
    #detect entities using deepavlov NER model
    params = proc_ents(globals.ner_model([msg]))
    #detect entities using regex
    params = params + detect_entities_regex(msg)
    #remove duplicates
    params = list({json.dumps(p):p for p in params}.values())
    return params

def process_linhas_apoio(linhas_apoio, assunto):
    regex = r'\btelevisao\b'

    if assunto == 'voz':
        regex += r'|\btele\w+'
    elif assunto == 'internet':
        regex += r'|\binternet\b'

    las = []
    for la in linhas_apoio:
        if re.search(regex, clean_msg(la['categoria'])):
            las.append(la)
    return las

def ntp_answer(idChat, msg):
    '''Get solution and parse it
    :param: id chat
    :param: user message
    '''
    answer = get_solver(idChat, msg)
    if answer:
        send_msg(idChat, answer['msg'])
        if answer['chat_id'] == -1:
            globals.redis_db.delete(idChat)
        elif answer['chat_id'] == -2:
            globals.redis_db.delete(idChat)
            linhas_apoio = get_content("/fs_scrapper/linhas_apoio", [], {})
            if linhas_apoio:
                if 'assunto' in answer:
                    linhas_apoio = process_linhas_apoio(linhas_apoio, answer['assunto'])
                pretty_print(idChat, "/fs_scrapper/linhas_apoio", linhas_apoio, True)
            else:
                send_msg(idChat, prefab_msgs["failed"][3])
    else:
        send_msg(idChat, prefab_msgs["failed"][2])

def modo_problemas(idChat, msg, chatData):
    '''Send to problem solver
    :param: id chat
    :param: user message
    :param: user chat state
    '''
    chatData["status"] = "modo problemas"
    globals.redis_db.set(idChat, json.dumps(chatData))
    ntp_answer(idChat, msg)

def get_location(idChat, idUser, msg, name, chatData, msg_params, entry, status, msg_ts, req_loc):
    '''Ask and interpret message in order to get user location
    :param: id chat
    :param: id user
    :param: user message
    :param: user name
    :param: user chat state
    :param: detected parameters in message
    :param: category entry in categories dict
    :param: user status if user not send location
    :param: message to send if user not send location
    :param: make show button in chat to user send location?
    '''
    loc = get_city(entry, msg_params)

    if loc:
        chatData["locationParam"] = {"search_term": loc}
        chatData["status"] = ""
        process_params(idChat, idUser, msg, name, chatData, msg_params)
    else:
        if status != "":
            chatData["status"] = status
            globals.redis_db.set(idChat, json.dumps(chatData))
            if req_loc:
                # pede ao utilizador a localização
                get_loc(idChat)
        else:
            globals.redis_db.delete(idChat)
        send_msg(idChat, msg_ts)

def ask_param(idChat, chatData):
    '''Choose and ask a parameter to user
    :param: id chat
    :param: user chat state
    '''
    msg = None

    if len(chatData["paramsMissingRequired"]):
        param_key, param_value = list(chatData["paramsMissingRequired"].items())[0]
        if isinstance(param_key, int):
            print("[LOG] Asking Required param (param_value): " + param_value)
            param = param_value
        else:
            print("[LOG] Asking Required param (param_key): " + param_key)
            param = param_key

        msg = pretty_question_required_param(param)
    elif len(chatData["paramsMissingOptional"]):
        param_key, param_value = list(chatData["paramsMissingOptional"].items())[0]
        print("[LOG] Asking Optional param (param_key): " + param_key)
        msg = pretty_question_optional_param(str(param_key))
        msg += prefab_msgs["request"][3]

    send_msg(idChat, msg)
    

def new_category_params(idChat, chatData, entry, msg_params):
    '''first process of params
    :param: id chat
    :param: user chat state
    :param: category entry in category dict
    :param: parameters detected in user message
    '''
    # process msg params, save
    required_params, missing_required_params, optional_params, missing_optional_params = detect_new_params(msg_params, entry, chatData)
    # adicionar ao redis
    add_new_params(chatData['paramsRequired'], required_params)
    add_new_params(chatData['paramsOptional'], optional_params)
    print("[LOG] Valid required "+str(chatData['paramsRequired']))
    print("[LOG] Valid optional "+str(chatData['paramsOptional']))

    # se for preciso pelo menos um param, envia um aviso ao user (e diz já a lista de params que terá)
    if entry['needAtLeastOneOptionalParam'] and len(chatData['paramsOptional']) == 0:
        print("[LOG] NeedAtLeastOneParam !!! ")
        warning_msg = "Esta busca precisará no mínimo de um destes campos:\n"
        for param in missing_optional_params:
            warning_msg += '-> ' + localizeToPT(param) + '\n'
        send_msg(idChat, warning_msg)

    # altera status e guarda (se faltam params pergunta logo um deles)
    if len(missing_required_params) or len(missing_optional_params):
        chatData["paramsStatus"] = "missing"
        chatData["paramsMissingRequired"] = missing_required_params
        chatData["paramsMissingOptional"] = missing_optional_params
        print("[LOG] Missing required "+str(chatData['paramsMissingRequired']))
        print("[LOG] Missing optional "+str(chatData['paramsMissingOptional']))

        if len(missing_required_params) == 0 and (not entry['needAtLeastOneOptionalParam'] or len(chatData['paramsOptional']) > 0) and len(missing_optional_params) > PARAM_THRESHOLD:
            querystrings_aux = merge_dicts(chatData["paramsOptional"], chatData['locationParam'])
            querystrings = merge_dicts(chatData["paramsRequired"], querystrings_aux)
            content = get_content(chatData["cat"], [], querystrings)

            if isinstance(content, list) and len(content) < 2:
                chatData["paramsMissingOptional"] = {}
                
            process_content(idChat, chatData, content)
        ask_param(idChat, chatData)
    else:
        chatData["paramsStatus"] = "done"

    globals.redis_db.set(idChat, json.dumps(chatData))

def save_param(idChat, msg, chatData, tp, msg_params):
    '''save param given by user
    :param: id chat
    :param: user message
    :param: user chat state
    :param: type ('Required' or 'Optional')
    '''
    first_key, first_type = list(chatData["paramsMissing" + tp].items())[0]

    paramsMissing = {
        'paramsRequired': chatData['paramsMissingRequired'],
        'paramsOptional': chatData['paramsMissingOptional']
    }
    required_params, missing_required_params, optional_params, missing_optional_params = detect_new_params(msg_params, paramsMissing, chatData)
    add_new_params(chatData['paramsRequired'], required_params)
    add_new_params(chatData['paramsOptional'], optional_params)

    chatData["paramsMissingRequired"] = missing_required_params
    chatData["paramsMissingOptional"] = missing_optional_params

    lr = len(required_params)
    lo = len(optional_params)

    m = clean_msg(msg)
    if tp == "Optional":
        if re.match(r'\bmostrar?\s+resultados?\b', m) or re.match(r'^/mostrar$', m):
            chatData['paramsMissingOptional'] = {}
        elif first_type == "PHONES_BOOLEAN":
            if re.match(r'\bs(im)?|y\b', m):
                chatData["params" + tp][first_key] = "yes"
                del chatData["paramsMissing" + tp][first_key]
            elif re.match(r'\bn(ao)?\b', m):
                del chatData["paramsMissing" + tp][first_key]
        elif not re.match(r'\bn(ao)?\b', m):
            if first_key not in optional_params and lr == 0 and lo == 0:
                chatData["params" + tp][first_key] = msg
                del chatData["paramsMissing" + tp][first_key]
        else:
            del chatData["paramsMissing" + tp][first_key]
    elif tp == "Required":
        if first_key not in required_params and lr == 0 and lo == 0:
            chatData["params" + tp][first_key] = msg
            del chatData["paramsMissing" + tp][first_key]

    globals.redis_db.set(idChat, json.dumps(chatData))

def missing_category_params(idChat, msg, chatData, msg_params):
    '''Process answer to requested parameter and asks another if necessary
    :param: id chat
    :param: user message
    :param: user chat state
    '''
    print("[DEBUG] adding param given by user")
    if len(chatData["paramsMissingRequired"]):
        save_param(idChat, msg, chatData, "Required", msg_params)
    elif len(chatData["paramsMissingOptional"]):
        save_param(idChat, msg, chatData, "Optional", msg_params)

    print("[LOG] Valid required "+str(chatData['paramsRequired']))
    print("[LOG] Valid optional "+str(chatData['paramsOptional']))
    print("[LOG] Missing required "+str(chatData['paramsMissingRequired']))
    print("[LOG] Missing optional "+str(chatData['paramsMissingOptional']))

    if len(chatData["paramsMissingRequired"]) or len(chatData["paramsMissingOptional"]):
        ask_param(idChat, chatData)
    else:
        chatData["paramsStatus"] = "done"

def process_params(idChat, idUser, msg, name, chatData, msg_params):
    '''Process parameters, question users when parameters are missing. When
    have all paremeters get content from the other modules. Finally send the
    content to user, sending messages
    :param: id chat
    :param: id user
    :param: user message
    :param: user name
    :param: user chat state
    :param: detected parameters in message
    '''
    entry = get_entry(chatData["cat"])
    location_params = entry['locationParam']

    # quanto o pedido nao recebe params, devolve resposta
    if not entry['paramsRequired'] and not entry['paramsOptional'] and not location_params:
        process_content(idChat, chatData, get_content(chatData["cat"], [], {}))
        globals.redis_db.delete(idChat)
    elif len(location_params) > 0 and chatData["locationParam"] == None and chatData["status"] != "gps_loc" and chatData["status"] != "search_loc":
        chatData['msg_params'] = msg_params
        get_location(idChat, idUser, msg, name, chatData, msg_params, entry, "gps_loc", "Qual a sua localização?", True)
    elif chatData["status"] == "gps_loc":
        get_location(idChat, idUser, msg, name, chatData, msg_params, entry, "search_loc", "Em que cidade se encontra?", False)
    elif chatData["status"] == "search_loc":
        get_location(idChat, idUser, msg, name, chatData, msg_params, entry, "", "Não foi possível perceber onde se encontra!", False)
    else:
        # new problem. save obtained params
        if chatData["paramsStatus"] == "new":
            if chatData['msg_params'] != {}:
                msg_params = chatData['msg_params']
                chatData['msg_params'] = {}
            new_category_params(idChat, chatData, entry, msg_params)
        # processing problem by asking and saving missing params
        elif chatData["paramsStatus"] == "missing":
            missing_category_params(idChat, msg, chatData, msg_params)

        # devolve resposta (todos os params foram obtidos), ou retorna falha (qd necessario minimo um param)
        if chatData["paramsStatus"] == "done":
            if entry['needAtLeastOneOptionalParam'] and len(chatData['paramsOptional']) == 0:
                send_msg(idChat, prefab_msgs["failed"][4])
            else:
                print("[LOG] All info collected. Sending response")
                querystrings_aux = merge_dicts(chatData["paramsOptional"], chatData['locationParam'])
                querystrings = merge_dicts(chatData["paramsRequired"], querystrings_aux)
                process_content(idChat, chatData, get_content(chatData["cat"], [], querystrings))
            globals.redis_db.delete(idChat)

def change_category(idChat, idUser, msg, name, chatData):
    '''Make the necessary changes according to user choice.
    :param: id chat
    :param: id user
    :param: user message
    :param: user name
    :param: user chat state
    :param: detected parameters
    '''
    muda_categoria = clean_msg(msg)

    # se o user quiser mudar, altera-se a categoria e marca-se como new para os params
    if re.match(r'\bs(im)?|y\b', muda_categoria):
        chatData["cat"] = chatData["cat_change"]
        chatData["paramsStatus"] = "new"
        chatData["paramsRequired"] = {}
        chatData["paramsOptional"] = {}
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

def ask_change_category(idChat, msg, chatData, cat):
    '''Ask user if want to change category
    :param: id chat
    :param: user message
    :param: user chat state
    :param: detected category
    '''
    chatData["status"] = "mudar categoria?"
    chatData["cat_change"] = cat
    chatData["cat_change_last_msg"] = msg
    globals.redis_db.set(idChat, json.dumps(chatData))
    entry1 = get_entry(chatData["cat"])
    entry2 = get_entry(cat)
    send_msg(idChat, "Pretende mudar de categoria de '" + entry1["prettyPrint"] + "' para '" + entry2["prettyPrint"] + "'? Responda por favor 'sim' ou 'não'")

def cannot_understand(idChat):
    '''Send messages so user can know that was not possible to understand what he/she wants.
    :param: id chat
    '''
    send_msg(idChat, prefab_msgs["failed"][5])
    send_msg(idChat, prefab_msgs["failed"][6])
    send_msg(idChat, prefab_msgs["failed"][7])
    linhas_apoio = get_content("/fs_scrapper/linhas_apoio", [], {})
    if linhas_apoio:
        pretty_print(idChat, "/fs_scrapper/linhas_apoio", linhas_apoio, True)
    else:
        send_msg(idChat, prefab_msgs["failed"][3])
    globals.redis_db.delete(idChat)

def get_response_default(idChat, idUser, msg, name, chatData):
    '''Intro of message in default mode. If intro changed category/functionality request him
    in order to know if wants to change. If after x tries was not possible to detect the
    category/functionality requests if user wants to use rules mode or if wants to call
    to support lines. On other cases the flow is passed to process_params
    :param: id chat
    :param: id user
    :param: user message
    :param: user name
    :param: user chat state
    '''
    if chatData["status"] == "mudar categoria?":
        change_category(idChat, idUser, msg, name, chatData)
    else:
        cat, confianca = get_categoria_frase(msg)
        print("[LOG] Category: " + cat + " with " + str(confianca) + " confidence")
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
                    process_params(idChat, idUser, msg, name, chatData, params)
            elif chatData["tries"] == tries - 1:
                cannot_understand(idChat)
            else:
                chatData["tries"] += 1
                globals.redis_db.set(idChat, json.dumps(chatData))
                send_msg(idChat, prefab_msgs["failed"][8])
        elif confianca > confianca_level:
            if chatData["cat"] == cat:
                process_params(idChat, idUser, msg, name, chatData, params)
            else:
                ask_change_category(idChat, msg, chatData, cat)
        else:
            process_params(idChat, idUser, msg, name, chatData, params)
