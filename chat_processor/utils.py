from categoria_dic import cat as dicionario
from config import urls
import requests, urllib.parse, unidecode

def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def clean_msg(msg):
    #mensagem toda em letras pequenas
    msg = msg.lower()

    #remover acentos
    msg = unidecode.unidecode(msg)

    return msg

#Dado uma funcionalidade devolve a entrada da mesma no dicionário
def get_entry(request):
    size = len(dicionario)
    i = 0
    found_value = None

    while i < size and found_value == None:
        if dicionario[i]['request'] == request:
            found_value = dicionario[i]
        i+=1

    return found_value

#Dado uma funcionalidade devolve o URL
def get_service(request):
    size = len(dicionario)
    i = 0
    found_service = None

    while i < size and found_service == None:
        if dicionario[i]['request'] == request:
            found_service = dicionario[i]['service']
        i+=1

    return urls[found_service]

#Faz um pedido ao API_ENDPOINT de forma a enviar uma msg ao utilizador
def send_msg(idChat, msg):
    URL = urls["API_ENDPOINT"] + "/send_message/" + urllib.parse.quote(str(idChat), safe='')

    print(URL)
    try:
        res = requests.post(URL, data=msg)
        res.raise_for_status()
        res = res.text
    except:
        res = None

    return res

#Faz um pedido ao API_ENDPOINT de forma a perguntar pela localização do utilizador
def get_loc(idChat):
    URL = urls["API_ENDPOINT"] + "/get_location/" + urllib.parse.quote(str(idChat), safe='')

    print(URL)
    try:
        res = requests.get(URL)
        res.raise_for_status()
        res = res.text
    except:
        res = None

    return res

#Faz um pedido a um URL, devolvendo a informação
# recebe como parâmetros:
#  - cat: a funcionalidade/categoria
#  - params: os parâmetros que vão no caminho (por ordem de aparição no caminho) (lista)
#  - querystrings: os parâmetros que vão nas querystrings (um dicionário chave valor)
def get_content(cat, params, querystrings):
    URL = get_service(cat)
    URL += cat

    size = len(params)
    i = 0
    if size > 0:
        for i in range(size):
            params[i] = urllib.parse.quote(str(params[i]), safe='')
        URL += "/".join(params)

    if len(querystrings) > 0:
        URL += "?"
        aux = []
        for (k,v) in querystrings.items():
            aux.append(urllib.parse.quote(k, safe='') + "=" + urllib.parse.quote(str(v), safe=''))
        URL += "&".join(aux)

    print(URL)
    try:
        res = requests.get(URL)
        res.raise_for_status()
        res = res.json()
        try:
            # O fs_scraper devolve o resultado no campo 'response'
            res = res.get('response', res)
        except:
            pass
    except:
        res = None

    return res
