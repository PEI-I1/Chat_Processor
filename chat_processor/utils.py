from categoria_dic import cat as dicionario
from config import urls
import requests, urllib.parse, unidecode

def clean_msg(msg):
    #mensagem toda em letras pequenas
    msg = msg.lower()

    #remover acentos
    msg = unidecode.unidecode(msg)

    return msg

#Recebe o contéudo em json altera para o formato de envio para o user
def process(content):
    msg_send = ""

    for (k,v) in content.items():
        if isinstance(v, list):
            msg_send += str(k).capitalize() +": "

            for i in range(0,len(v)):
                if(i == len(v)-1):
                    msg_send += str(v[i])
                else:
                    msg_send += str(v[i]) + ", "

        else:
            msg_send += str(k).capitalize() + ": " + str(v) + "\n"
    return msg_send

x = process({"link":"https://www.nos.pt/particulares/loja-equipamentos/pages/details.aspx?p=30343","nome":"Xiaomi Mi 9T","pontos":"Dispon\u00edvel","preco":"389,98","pretacoes":"Dispon\u00edvel","tags":["novidade","Oportunidade Presta\u00e7\u00f5es","asda","erwer"]})
print(x)

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
