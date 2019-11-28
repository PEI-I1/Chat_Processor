from categoria_dic import cat as dicionario
from config import urls
import requests, urllib.parse, unidecode

def clean_msg(msg):
    #mensagem toda em letras pequenas
    msg = msg.lower()

    #remover acentos
    msg = unidecode.unidecode(msg)

    return msg

#Recebe a lista e devolve os 5 primeiros elementos formatados a enviar ao user
def process_list(content):
    n = 0
    size = len(content)
    msg_send = ""

    while n < size and n < 5:
        for key in content[n]:
            msg_send += key + ": " + content[n][key] + "\n"
        n += 1
        msg_send += "\n"

    if n == 5:
        msg_send += "Se pretender ver o resto das opções escreva 'ver mais'."
    return msg_send

#Recebe a lista e devolve-a formatada a enviar ao user
def process_all_list(content):
    msg_send = ""

    for elem in content:
        for key in elem:
            msg_send += key + ": " + elem[key] + "\n"
        msg_send += "\n"

    return msg_send

#Dado uma funcionalidade devolve o URL
def get_service(request):
    size = len(dicionario)
    i = 0
    found_service = None

    while i < size and found_service == None:
        if dicionario[i]['request'] == request:
            found_service = dicionario[i]['service']

    return urls[found_service]

#Dado uma funcionalidade devolve os params necessários
def get_params_required(request):
    size = len(dicionario)
    i = 0
    found_params = None

    while i < size and found_params == None:
        if dicionario[i]['request'] == request:
            found_params = dicionario[i]['paramsRequired']

    return found_params

#Dado uma funcionalidade devolve os params necessários
def get_params_optional(request):
    size = len(dicionario)
    i = 0
    found_params_opt = None

    while i < size and found_params_opt == None:
        if dicionario[i]['request'] == request:
            found_params_opt = dicionario[i]['paramsOptional']

    return found_params_opt

# dado uma funcionalidade devolve os parãmetros relativos à localização
def get_params_location(request):
    size = len(dicionario)
    i = 0
    found_loc_params = None

    while i < size and found_loc_params == None:
        if dicionario[i]['request'] == request:
            found_loc_params = dicionario[i]['locationParam']

    return found_loc_params

# dado uma funcionalidade devolve o valor do 'needAtLeastOneOptionalParam'
def get_needAtLeastOneOptionalParam(request):
    size = len(dicionario)
    i = 0
    value = None

    while i < size and value == None:
        if dicionario[i]['request'] == request:
            value = dicionario[i]['needAtLeastOneOptionalParam']
    return value


# dado uma funcionalidade devolve a frase a ser usada quando faltam params obrigatórios
def get_phrase_missing_param(cat):
    size = len(dicionario)
    i = 0
    foundPhrase = None

    while i < size and foundPhrase == None:
        if dicionario[i]['request'] == cat:
            foundPhrase = dicionario[i]['phraseMissingParams']

    return foundPhrase

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
            params[i] = urllib.parse.quote(params[i], safe='')
            i+=1

        URL += "/".join(params)

    if len(querystrings) > 0:
        URL += "?"
        aux = []
        for (k,v) in querystrings:
            aux.append(urllib.parse.quote(k, safe='') + "=" + urllib.parse.quote(v, safe=''))
        URL += "&".join(aux)

    print(URL)
    try:
        res = requests.get(URL)
        res.raise_for_status()
        res = res.json().get('response')
    except:
        res = None

    return res
