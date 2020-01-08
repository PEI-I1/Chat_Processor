from categoria_dic import cat as dicionario
from config import urls
import requests, urllib.parse, unidecode, globals, json

def merge_dicts(x, y):
    '''Merge two dictionaries
    :param: a dictionary
    :param: another dictionary
    :return: merged dictionary
    '''
    z = x.copy()
    if y:
        z.update(y)
    return z

def clean_msg(msg):
    '''Cleans a message, removing accents and uppercases
    :param: text/message to clean
    :return: clean message
    '''
    #mensagem toda em letras pequenas
    msg = msg.lower()

    #remover acentos
    msg = unidecode.unidecode(msg)

    return msg

def get_entry(request):
    '''For a given category/functionality returns its entry
    in categories/functionalities dictionary (categoria_dict)
    :param: name/path of category/functionality
    :return: category/functionality entry
    '''
    size = len(dicionario)
    i = 0
    found_value = None

    while i < size and found_value == None:
        if dicionario[i]['request'] == request:
            found_value = dicionario[i]
        i+=1

    return found_value

def get_service(request):
    '''For a given category/functionality returns its URL
    in categories/functionalities dictionary (categoria_dict)
    :param: name/path of category/functionality
    :return: category/functionality URL
    '''
    size = len(dicionario)
    i = 0
    found_service = None

    while i < size and found_service == None:
        if dicionario[i]['request'] == request:
            found_service = dicionario[i]['service']
        i+=1

    return urls[found_service]

def get_solver(idChat, msg):
    '''Makes a request to Problems Resolution module in order to 
    answer a user message
    :param: id chat
    :param: user message
    :return: Problems Resolution module response or None
    '''
    URL = urls["RS"] + "/solver"

    print(URL)
    try:
        res = requests.post(URL, json={"idChat": idChat, "msg": msg})
        res.raise_for_status()
        res = res.json()
    except:
        res = None

    return res

def send_msg(idChat, msg):
    '''Makes a request to API Endpoint in order do send a message to user
    :param: id chat
    :param: message to send to user
    :return: API Endpoint response or None
    '''
    URL = urls["API_ENDPOINT"] + "/send_message/" + urllib.parse.quote(str(idChat), safe='')

    print(URL)
    try:
        res = requests.post(URL, data=msg.encode("utf-8"))
        res.raise_for_status()
        res = res.text
    except:
        res = None

    return res

def send_photo(idChat, msg):
    '''Makes a request to API Endpoint in order do send a photo with captions to user
    :param: id chat
    :param: photo and captions to send to user
    :return: API Endpoint response or None
    '''
    URL = urls["API_ENDPOINT"] + "/send_photo/" + urllib.parse.quote(str(idChat), safe='')

    print(URL)
    try:
        res = requests.post(URL, data=msg.encode("utf-8"))
        res.raise_for_status()
        res = res.text
    except:
        res = None

    return res


def send_menu(idChat, msg, reply_json):
    '''Makes a request to API Endpoint in order do send a inline keyboard to user
    :param: id chat
    :param: message to send to user
    :param: keyboard to send to user
    :return: API Endpoint response or None
    '''
    URL = urls["API_ENDPOINT"] + "/send_keyboard/" + urllib.parse.quote(str(idChat), safe='')

    print(URL)
    try:
        info = {}
        info['text'] = msg
        info['keyboard'] = reply_json
        info = json.dumps(info)
        res = requests.post(URL, data=info.encode("utf-8"))
        res.raise_for_status()
        res = res.text
    except:
        res = None

    return res


def get_loc(idChat):
    '''Makes a request to API Endpoint in order to request user GPS location
    :param: id chat
    :return: API Endpoint response or None
    '''
    URL = urls["API_ENDPOINT"] + "/get_location/" + urllib.parse.quote(str(idChat), safe='')

    print(URL)
    try:
        res = requests.get(URL)
        res.raise_for_status()
        res = res.text
    except:
        res = None

    return res

def get_content(cat, params, querystrings):
    '''Makes a request to an URL (depending on category/functionality) in order to obtain
    information from that category/functionality
    :param: category/functionality
    :param: list of parameters that goes in path (in order of ocorrence in path)
    :param: a dictionary of query string parameters 
    :return: Category/Functionality response or None
    '''
    URL = get_service(cat)
    URL += cat

    size = len(params)
    i = 0
    if size > 0:
        for i in range(size):
            params[i] = urllib.parse.quote(str(params[i]), safe='')
        URL += "/".join(params) if URL[-1] == "/" else "/" + "/".join(params)

    if len(querystrings) > 0:
        URL += "?"
        aux = []
        for (k,v) in querystrings.items():
            aux.append(urllib.parse.quote(k, safe='') + "=" + urllib.parse.quote(str(v), safe=''))
        URL += "&".join(aux)

    print("[LOG] get_content from: "+URL)
    try:
        res = requests.get(URL)
        res.raise_for_status()
        res = res.json()
    except:
        res = None

    return res
