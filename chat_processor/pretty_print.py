from utils import send_msg, send_photo, clean_msg
from prefab_msgs import prefab_msgs
import json, re, globals


def bold(text):
    '''For a given text make a html bold of it
    :param: text to bold
    '''
    return "<b>" + text + "</b>"

def linhas_apoio(idChat, content, cat):
    '''Pretty print of support lines
    :param: id chat to send the messages
    :param: content of messages
    '''
    send_msg(idChat, 'As linhas de apoio da NOS são:\n')

    for l in content:
        s = bold(l["categoria"]) + "\n"
        s += bold("Contacto: ") + l["numero"] + "\n"
        s += l["horario"] + "\n"
        if 'preco' in l:
            s += bold("Custo da chamada: ") + l["preco"] + "\n"
        send_msg(idChat, s)

def phones(idChat, content, cat):
    '''Pretty print of phones
    :param: id chat to send the messages
    :param: content of messages
    '''
    send_msg(idChat, 'Os telemóveis que correspondem à procura são:')

    for p in content:
        s = bold("Nome: ") + p["nome"] + "\n"
        s += bold("Preço: ") + p["preco"] + " €"
        if 'preco_original' in p:
            s += ' (custava ' + p['preco_original'] + ' €)\n'
        else:
            s += '\n'
        if 'processador' in p and p['processador']:
             s += bold("Processador: ") + p["processador"] + "\n"
        if 'memoria' in p and p['memoria']:
             s += bold("Memória: ") + p["memoria"] + "\n"
        if 'camara' in p and p['camara']:
            s += bold("Câmara: ") + "\n         " + p["camara"] + "\n"
        if 'oferta' in p:
            s += bold("Oferta: ") + p["oferta"] + "\n"
        if 'tags' in p:
            for t in p['tags']:
                if 'oferta' in t:
                    s += bold("Oferta: ") + t + "\n"
        if 'pontos' in p:
            s += bold("Comprar com pontos: ") + p["pontos"] + "\n"
        if 'prestacoes' in p:
            s += bold("Comprar às prestações: ") + p["prestacoes"] + "\n"
        s += bold("Link para comprar: ") + p["link"]
        if 'image_link' in p and p['image_link']:
            msg = json.dumps({
                'photo': p['image_link'],
                'caption': s
            })
            send_photo(idChat, msg)
        else:
            send_msg(idChat, s)

def wtf(idChat, content, cat):
    '''Pretty print of WTF tariffs
    :param: id chat to send the messages
    :param: content of messages
    '''
    send_msg(idChat, 'Os pacotes WTF que correspondem à procura são:')

    for t in content:
        s = bold("Nome: ") + t["nome"] + "\n"
        s += bold("Preço: ") + t["preco"] + "\n"
        if "preco_total" in t:
            s += bold("Preço/mês: ") + t["preco_total"] + " €\n"
        s += bold("Net: ") + t["net"] + "\n"
        s += bold("SMS: ") + t["sms"] + "\n"
        s += bold("Chamadas: ") + t["minutos"] + "\n"
        if "cinema" in t:
            s += bold("Cinemas: ") + t["cinema"] + "\n"
        if "uber" in t:
            s += bold("Uber: ") + t["uber"] + "\n"
        if "uber_eats" in t:
            s += bold("Uber Eats: ") + t["uber_eats"]
        send_msg(idChat, s)

def stores(idChat, content, cat):
    '''Pretty print of stores
    :param: id chat to send the messages
    :param: content of messages
    '''
    send_msg(idChat, "As lojas NOS que correspondem à procura são:")

    for l in content:
        s = bold("Nome: ") + l["nome"] + "\n"
        s += bold("Morada: ") + l["morada"] + "\n"
        h = re.split("(.*?\d{2}h\d{2} - \d{2}h\d{2})", l["horario"])
        h = list(filter(None, h))
        s += bold("Horário: ") + "\n               ".join(h)
        send_msg(idChat, s)

def packages(idChat, content, cat):
    '''Pretty print of packages
    :param: id chat to send the messages
    :param: content of messages
    '''
    send_msg(idChat, "Os pacotes NOS que correspondem à procura são:")

    for p in content:
        s = bold("Nome: ") + p["nome"] + "\n"
        if "Tipo" in p:
            s += bold("Tipo: ") + p["Tipo"] + "\n"
        if "servico" in p:
            s += bold("Serviço: ") + p["servico"] + "\n"
        if "canais" in p and p["canais"]:
            s += bold("Canais: ") + p["canais"] + "\n"
        if "net" in p and p["net"]:
            s += bold("Net: ") + p["net"] + "\n"
        if "phone" in p and p["phone"]:
            s += bold("Telefone: ") + p["phone"] + "\n"
        if "mobile" in p and p["mobile"]:
            s += bold("Telemóvel: ") + p["mobile"] + "\n"
        if "netMovel" in p and p["netMovel"]:
            s += bold("Net Móvel: ") + p["netMovel"] + "\n"
        if "preco" in p:
            s += bold("Preço: ") + p["preco"] + " €"
        send_msg(idChat, s)

        fids = ["Fidelizacao_24Meses", "Fidelizacao_12Meses", "Fidelizacao_6Meses"]
        for fid in fids:
            if fid in p:
                aux = p[fid]

                s = "Com " + bold(aux["Fidelizacao"]) + " de fidelização:\n"
                s += bold("Preço: ") + aux["preco"] + " €\n"
                s += bold("Preço de Adesão: ") + aux["precoAdesao"] + " €\n"
                s += bold("Vantagens:\n") + "\n".join(aux["Vantagens"])
                send_msg(idChat, s)

        if "Sem_Fidelizacao" in p:
            aux = p["Sem_Fidelizacao"]

            s = "Sem fidelização:\n"
            s += bold("Preço: ") + aux["preco"] + " €\n"
            s += bold("Preço de Adesão: ") + aux["precoAdesao"] + " €\n"
            s += bold("Vantagens:\n") + "\n".join(aux["Vantagens"])
            send_msg(idChat, s)

def cinemas(idChat, content, cat):
    '''Pretty print of closest cinemas
    :param: chat id to send the messages to
    :param: content of messages
    '''
    if len(content["cinemas"]):
        s = 'Os cinemas NOS mais perto de ti são:\n'
        s += " - " + "\n - ".join(content["cinemas"])
        send_msg(idChat, s)
    else:
        send_msg(idChat, prefab_msgs["failed"][9])

def movies_search(idChat, content, cat):
    '''Pretty print of a search for movies
    :param: id chat to send the messages
    :param: content of messages
    '''
    send_msg(idChat, 'Os filmes que cumprem a pesquisa são:')

    for m in content:
        s = bold("Título: ") + m["Portuguese title"] + "\n"
        s += bold("Título original: ") + m["Original title"] + "\n"
        s += bold("IMDB Rating: ") + m["IMDB Rating"] + "\n"
        s += bold("Elenco: ") + m["Cast"] + "\n"
        s += bold("Realizador: ") + m["Producer"] + "\n"
        s += bold("Género: ") + m["Genre"] + "\n"
        s += bold("Duração: ") + str(m["Length (min)"]) + " minutos\n"
        s += bold("Idade: ") + str(m["Age rating"]) + " anos\n"
        s += bold("Sinopse: ") + m["Synopsis"] + "\n"
        s += bold("Trailer: ") + m["Trailer"] + "\n"
        photo = m["Banner"]

        msg = json.dumps({
            'photo': photo,
            'caption': s
        })
        send_photo(idChat, msg)

def releases(idChat, content, cat):
    '''Pretty print of movie releases
    :param: id chat to send the messages
    :param: content of messages
    '''
    send_msg(idChat, 'As próximas estreias dos cinemas NOS são:')

    for m in content:
        s = bold("Título: ") + m["Original title"] + "\n"
        s += bold("IMDB Rating: ") + m["IMDB Rating"] + "\n"
        s += bold("Realizador: ") + m["Producer"] + "\n"
        s += bold("Elenco: ") + m["Cast"] + "\n"
        s += bold("Género: ") + m["Genre"] + "\n"
        s += bold("Trailer: ") + m["Trailer"] + "\n"
        photo = m["Banner"]

        msg = json.dumps({
            'photo': photo,
            'caption': s
        })
        send_photo(idChat, msg)

def movie_details(idChat, content, cat):
    '''Pretty print of a movie
    :param: id chat to send the messages
    :param: content of messages
    '''
    m = content[0]

    s = bold("Título: ") + m["Portuguese title"] + "\n"
    s += bold("Título original: ") + m["Original title"] + "\n"
    s += bold("IMDB Rating: ") + m["IMDB Rating"] + "\n"
    s += bold("Elenco: ") + m["Cast"] + "\n"
    s += bold("Realizador: ") + m["Producer"] + "\n"
    s += bold("Género: ") + m["Genre"] + "\n"
    s += bold("Duração: ") + str(m["Length (min)"]) + " minutos\n"
    s += bold("Idade: ") + str(m["Age rating"]) + " anos\n"
    s += bold("Sinopse: ") + m["Synopsis"] + "\n"
    s += bold("Trailer: ") + m["Trailer"] + "\n"
    photo = m["Banner"]

    msg = json.dumps({
        'photo': photo,
        'caption': s
    })
    send_photo(idChat, msg)

def ask_cinema(idChat, content, cat):
    '''Ask user to select a cinema
    :param: id chat
    :param: content to filter
    :param: category detected
    '''
    n = 1
    m = 'Escolha um dos cinemas:\n'
    m += "    0. Nenhuma das hipóteses\n"
    cinemas = []

    for c in content:
        m += "    " + str(n) + ". " + c + "\n"
        cl = clean_msg(c)
        words = cl.split()
        l = len(words)
        s = set()
        while l > 0:
            s.add(" ".join(words[0:l]))
            l -= 1
            s.add(words[l])
        for w in list(s):
            cinemas.append({'choice': n, 'match': w})
        n += 1

    m += "Indique o número ou o nome do cinema."
    globals.redis_db.set("content" + str(idChat), json.dumps({'cat': cat, 'value': content, 'keys': cinemas}))
    send_msg(idChat, m)

def print_with_ask_cinema(idChat, content, cat, titleF, print_session):
    '''Print or ask user for cinema
    :param: id chat
    :param: content to filter
    :param: category detected
    :param: function to save and print title
    :param: function to print a session
    '''
    if isinstance(content, list):
        for m in content:
            print_session(idChat, m)
    else:
        if len(content) <= 1:
            titleF(idChat, content, cat)
            ver_mais(idChat)
        else:
            ask_cinema(idChat, content, cat)

def title(idChat, content, cat, c):
    '''Set "ver mais" and send title to user acording to category
    :param: id chat
    :param: content to filter
    :param: category detected
    :param: cinema selected
    '''
    prefix = '/scrapper/sessions/'
    if cat == prefix + "by_duration" or cat == prefix + "next_sessions":
        globals.redis_db.set("vermais" + str(idChat), json.dumps({'cat': cat, 'content': content[c]}))
        send_msg(idChat, 'Próximas sessões no ' + c + ':')
    elif cat == prefix + "by_movie":
        for m in content[c]:
            globals.redis_db.set("vermais" + str(idChat), json.dumps({'cat': cat, 'content': content[c][m]['sessions']}))
            send_msg(idChat, 'Próximas sessões do filme "' + m + '" no ' + c + ':')
    elif cat == prefix + "by_date":
        globals.redis_db.set("vermais" + str(idChat), json.dumps({'cat': cat, 'content': content[c]}))
        send_msg(idChat, 'Sessões no ' + c + ':')
    elif cat == '/scrapper/movies/by_cinema':
        globals.redis_db.set("vermais" + str(idChat), json.dumps({'cat': cat, 'content': content[c]}))
        send_msg(idChat, 'Os filmes em exibição no ' + c + ' são:')

def movie_of_movies_by_cinema(idChat, m):
    '''Pretty print of a movie from movies of a cinema
    :param: a movie
    '''
    s = bold('Título: ') + m['Portuguese title'] + "\n"
    s += bold('IMDB Rating: ') + m['IMDB Rating']
    send_msg(idChat, s)

def movies_by_cinema(idChat, content, cat):
    '''Pretty print of movies on display in cinema
    :param: chat id to send the messages to
    :param: content of messages
    '''
    def aux(idChat, content, cat):
        for c in content:
            title(idChat, content, cat, c)

    print_with_ask_cinema(idChat, content, cat, aux, movie_of_movies_by_cinema)

def session_of_sessions_by_duration(idChat, m):
    '''Pretty print of a session from sessions with a specific duration on cinemas
    :param: a session
    '''
    s = bold("Filme: ") + m["Movie"] + "\n"
    s += bold("Data: ") + m["Start date"] + "\n"
    s += bold("Hora de início: ") + m["Start time"] + "\n"
    s += bold("Duração: ") + str(m["Length (min)"]) + " minutos\n"
    s += bold("Lugares disponíveis: ") + m["Availability"] + "\n"
    s += bold("Link de compra: ") + m["Ticket link"] + "\n"
    send_msg(idChat, s)

def sessions_by_duration(idChat, content, cat):
    '''Pretty print of sessions with a specific duration on cinemas
    :param: id chat to send the messages
    :param: content of messages
    '''
    def aux(idChat, content, cat):
        for c in content:
            title(idChat, content, cat, c)

    print_with_ask_cinema(idChat, content, cat, aux, session_of_sessions_by_duration)

def session_of_next_sessions(idChat, m):
    '''Pretty print of a session from next sessions on cinemas
    :param: a session
    '''
    s = bold("Filme: ") + m["Movie"] + "\n"
    s += bold("Data: ") + m["Start date"] + "\n"
    s += bold("Hora de início: ") + m["Start time"] + "\n"
    s += bold("Lugares disponíveis: ") + m["Availability"] + "\n"
    s += bold("Trailer: ") + m["Trailer"] + "\n"
    s += bold("Link de compra: ") + m["Ticket link"] + "\n"
    send_msg(idChat, s)

def next_sessions(idChat, content, cat):
    '''Pretty print of next sessions on cinemas
    :param: id chat to send the messages
    :param: content of messages
    '''
    def aux(idChat, content, cat):
        for c in content:
            title(idChat, content, cat, c)

    print_with_ask_cinema(idChat, content, cat, aux, session_of_next_sessions)

def session_of_sessions_by_movie(idChat, s):
    '''Pretty print of a session from sessions for a specific movie on cinemas
    :param: a session
    '''
    st = bold("Data: ") + s["Start date"] + "\n"
    st += bold("Hora de início: ") + s["Start time"] + "\n"
    st += bold("Lugares disponíveis: ") + s["Availability"] + "\n"
    st += bold("Link de compra: ") + s["Ticket link"] + "\n"
    send_msg(idChat, st)

def sessions_by_movie(idChat, content, cat):
    '''Pretty print of sessions for a specific movie on cinemas
    :param: id chat to send the messages
    :param: content of messages
    '''
    def aux(idChat, content, cat):
        for c in content:
            title(idChat, content, cat, c)

    print_with_ask_cinema(idChat, content, cat, aux, session_of_sessions_by_movie)

def session_of_sessions_by_date(idChat, m):
    '''Pretty print of a session from sessions with a specific date on cinemas
    :param: a session
    '''
    s = bold("Filme: ") + m["Movie"] + "\n"
    s += bold("Data: ") + m["Start date"] + "\n"
    s += bold("Hora de início: ") + m["Start time"] + "\n"
    s += bold("Lugares disponíveis: ") + m["Availability"] + "\n"
    s += bold("Link de compra: ") + m["Ticket link"] + "\n"
    send_msg(idChat, s)

def sessions_by_date(idChat, content, cat):
    '''Pretty print of sessions with a specific date on cinemas
    :param: id chat to send the messages
    :param: content of messages
    '''
    def aux(idChat, content, cat):
        for c in content:
            title(idChat, content, cat, c)

    print_with_ask_cinema(idChat, content, cat, aux, session_of_sessions_by_date)


switcher = {
    '/fs_scrapper/linhas_apoio': linhas_apoio,
    '/fs_scrapper/phones': phones,
    '/fs_scrapper/wtf': wtf,
    '/fs_scrapper/stores': stores,
    '/fs_scrapper/packages': packages,
    '/scrapper/cinemas/search': cinemas,
    '/scrapper/movies/by_cinema': movies_by_cinema,
    '/scrapper/movies/search': movies_search,
    '/scrapper/movies/releases': releases,
    '/scrapper/movies/details': movie_details,
    '/scrapper/sessions/by_duration': sessions_by_duration,
    '/scrapper/sessions/next_sessions': next_sessions,
    '/scrapper/sessions/by_movie': sessions_by_movie,
    '/scrapper/sessions/by_date': sessions_by_date
}


def pretty_print(idChat, cat, content, allInfo):
    '''Pretty print of a content, sending pretty messages to user
    :param: id chat to send the messages
    :param: category of content
    :param: content of messages
    :param: should send all information?
    '''
    ret = None

    if content:
        if isinstance(content, str):
            send_msg(idChat, content)
        elif isinstance(content, list) and not allInfo:
            func = switcher.get(cat, send_msg)
            func(idChat, content[0:5], cat)
            send_msg(idChat, prefab_msgs["request"][2])
        else:
            func = switcher.get(cat, send_msg)
            func(idChat, content, cat)
    else:
        send_msg(idChat, 'Não foi possível dar resposta ao seu pedido.')


def ver_mais(idChat):
    '''When lists are too long only shows first 5 elements
    :param: id chat
    '''
    verMaisAux = globals.redis_db.get("vermais" + str(idChat))
    if verMaisAux:
        c = json.loads(verMaisAux)
        info_left = len(c["content"]) > 5
        pretty_print(idChat, c["cat"], c["content"][:5], not info_left)
        if info_left:
            c["content"] = c["content"][5:]
            globals.redis_db.set("vermais" + str(idChat), json.dumps(c))
        else:
            globals.redis_db.delete("vermais" + str(idChat))
    else:
        send_msg(idChat, prefab_msgs["failed"][10])
