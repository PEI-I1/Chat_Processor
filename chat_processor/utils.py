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
raul_test_this = {"Braga Parque": {"Countdown": {"sessions": [{"Start date": "2019-12-04", "Start time": "16:50:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000318&DataSessao=2019-12-04&HoraSessao=16:50&Sala=5"}, {"Start date": "2019-12-04", "Start time": "19:20:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000318&DataSessao=2019-12-04&HoraSessao=19:20&Sala=5"}, {"Start date": "2019-12-04", "Start time": "22:00:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000318&DataSessao=2019-12-04&HoraSessao=22:00&Sala=5"}, {"Start date": "2019-12-04", "Start time": "00:40:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000318&DataSessao=2019-12-05&HoraSessao=00:40&Sala=5"}]}, "Frozen II": {"sessions": [{"Start date": "2019-12-04", "Start time": "18:40:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1984110&DataSessao=2019-12-04&HoraSessao=18:40&Sala=3"}, {"Start date": "2019-12-04", "Start time": "21:20:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1733660&DataSessao=2019-12-04&HoraSessao=21:20&Sala=3"}, {"Start date": "2019-12-04", "Start time": "00:00:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1733660&DataSessao=2019-12-05&HoraSessao=00:00&Sala=3"}]}, "Joker": {"sessions": [{"Start date": "2019-12-04", "Start time": "18:30:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1733470&DataSessao=2019-12-04&HoraSessao=18:30&Sala=2"}, {"Start date": "2019-12-04", "Start time": "21:30:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1733470&DataSessao=2019-12-04&HoraSessao=21:30&Sala=2"}, {"Start date": "2019-12-04", "Start time": "00:30:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1733470&DataSessao=2019-12-05&HoraSessao=00:30&Sala=2"}]}, "Knives Out": {"sessions": [{"Start date": "2019-12-04", "Start time": "17:50:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000338&DataSessao=2019-12-04&HoraSessao=17:50&Sala=4"}, {"Start date": "2019-12-04", "Start time": "21:10:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000338&DataSessao=2019-12-04&HoraSessao=21:10&Sala=4"}, {"Start date": "2019-12-04", "Start time": "00:15:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000338&DataSessao=2019-12-05&HoraSessao=00:15&Sala=4"}]}, "Le Mans 66'": {"sessions": [{"Start date": "2019-12-04", "Start time": "17:10:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000321&DataSessao=2019-12-04&HoraSessao=17:10&Sala=7"}, {"Start date": "2019-12-04", "Start time": "20:40:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000321&DataSessao=2019-12-04&HoraSessao=20:40&Sala=7"}, {"Start date": "2019-12-04", "Start time": "00:05:00", "Availability": "0"}, {"Start date": "2019-12-04", "Start time": "00:35:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000335&DataSessao=2019-12-05&HoraSessao=00:35&Sala=6"}]}, "Danger Close: The Battle of Long Tan": {"sessions": [{"Start date": "2019-12-04", "Start time": "21:00:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000328&DataSessao=2019-12-04&HoraSessao=21:00&Sala=1"}, {"Start date": "2019-12-04", "Start time": "23:50:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1000328&DataSessao=2019-12-04&HoraSessao=23:50&Sala=1"}]}, "Playing with Fire": {"sessions": [{"Start date": "2019-12-04", "Start time": "19:00:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1736700&DataSessao=2019-12-04&HoraSessao=19:00&Sala=9"}, {"Start date": "2019-12-04", "Start time": "21:50:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1736700&DataSessao=2019-12-04&HoraSessao=21:50&Sala=9"}, {"Start date": "2019-12-04", "Start time": "00:20:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1736700&DataSessao=2019-12-05&HoraSessao=00:20&Sala=9"}]}, "Tristeza e Alegria na Vida das Girafas": {"sessions": [{"Start date": "2019-12-04", "Start time": "18:10:00", "Availability": "0", "Ticket link": "https://bilheteira.cinemas.nos.pt/webticket/bilhete.jsp?CinemaId=WA&CodFilme=1737960&DataSessao=2019-12-04&HoraSessao=18:10&Sala=1"}]}}}
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
