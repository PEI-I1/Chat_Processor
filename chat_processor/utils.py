from categoria_dic import cat as dicionario
from config import urls
import requests, urllib.parse

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
def get_service(cat):
    size = len(dicionario)
    i = 0
    foundCat = None

    while i < size and foundCat == None:
        if dicionario[i]['request'] == cat:
            foundCat = dicionario[i]['service']

    return urls[foundCat]

#Dado uma funcionalidade devolve os params necessários
def get_params(cat):
    size = len(dicionario)
    i = 0
    foundCat = None

    while i < size and foundCat == None:
        if dicionario[i]['request'] == cat:
            foundCat = dicionario[i]['params']

    return foundCat

#Faz um pedido a um URL, devolvendo o data
def get_content(URL):
    '''recebe um pedido e retorna a informação '''
    try:
        res = requests.get(URL)
        res.raise_for_status()
        res = res.json().get('response')
    except:
        res = None
    return res
