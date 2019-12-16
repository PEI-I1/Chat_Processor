from utils import send_msg, send_photo
import json, re

def bold(text):
    return "<b>" + text + "</b>"

def linhas_apoio(idChat, content):
    s = 'As linhas de apoio da NOS são:\n'
    s += "\n".join(map(lambda l: bold(l["categoria"] + ": ") + l["numero"], content))
    send_msg(idChat, s)

def phones(idChat, content):
    send_msg(idChat, 'Os telemóveis que correspondem à procura são:')

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + " €\n"
        if 'oferta' in p:
            s += bold("Oferta: ") + content["oferta"] + "\n"
        if 'tags' in p:
            for t in p['tags']:
                if 'oferta' in t:
                    s += bold("Oferta: ") + t + "\n"
        if 'pontos' in p:
            s += bold("Comprar com pontos: ") + content["pontos"] + "\n"
        if 'pretacoes' in p:
            s += bold("Comprar às prestações: ") + content["pretacoes"] + "\n"
        s += bold("Link para comprar: ") + content["link"]
        send_msg(idChat, s)

def wtf(idChat, content):
    send_msg(idChat, 'Os pacotes WTF que correspondem à procura são:')

    for t in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + "\n"
        if "preco_total" in t:
            s += bold("Preço/mês: ") + content["preco_total"] + " €\n"
        s += bold("Net: ") + content["net"] + "\n"
        s += bold("SMS: ") + content["sms"] + "\n"
        s += bold("Chamadas: ") + content["minutos"] + "\n"
        if "cinema" in t:
            s += bold("Cinemas: ") + content["cinema"] + "\n"
        if "uber" in t:
            s += bold("Uber: ") + content["uber"] + "\n"
        if "uber_eats" in t:
            s += bold("Uber Eats: ") + content["uber_eats"]
        send_msg(idChat, s)

def stores(idChat, content):
    send_msg(idChat, "As lojas NOS que correspondem à procura são:")

    for l in content:
        s = bold("Nome: ") + l["nome"] + "\n"
        s += bold("Morada: ") + l["morada"] + "\n"
        h = re.split("(.*?\d{2}h\d{2} - \d{2}h\d{2})", l["horario"])
        h = list(filter(None, h))
        s += bold("Horário: ") + "\n               ".join(h)
        send_msg(idChat, s)

def packages(idChat, content):
    send_msg(idChat, "Os pacotes NOS que correspondem à procura são:")

    for p in content:
        s = bold("Nome: ") + p["nome"] + "\n"
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
            s += bold("Preço: ") + aux["preco"] + " €"
        send_msg(idChat, s)

        fids = ["Fidelizacao_24Meses", "Fidelizacao_12Meses", "Fidelizacao_6Meses"]
        for fid in fids:
            if fid in p:
                aux = p[fid]

                s = "Com " + bold(aux["Fidelizacao"]) + " de fidelização:\n"
                s += bold("Preço: ") + aux["preco"] + " €\n"
                s += bold("Preço de Adesão: ") + aux["precoAdesao"] + " €\n"
                s += bold("Vantagens:\n") + "\n".join(aux["vantagens"])
                send_msg(idChat, s)

        if "Sem_Fidelizacao" in p:
            aux = p["Sem_Fidelizacao"]

            s = "Sem fidelização:\n"
            s += bold("Preço: ") + aux["preco"] + " €\n"
            s += bold("Preço de Adesão: ") + aux["precoAdesao"] + " €\n"
            s += bold("Vantagens:\n") + "\n".join(aux["vantagens"])
            send_msg(idChat, s)

def cinemas(idChat, content):
    s = 'Os cinemas NOS perto de si são:\n'
    s += "\n".join(content["cinemas"])
    send_msg(idChat, s) 

def movies_by_cinema(idChat, content):
    for c in content:
        s = 'Os filmes em exibição no ' + c + ' são:\n'
        s += "\n".join(content[c])
        send_msg(idChat, s)

def movies_search(idChat, content):
    send_msg(idChat, 'Os filmes que cumprem a pesquisa são:')

    for m in content:
        s = bold("Título: ") + m["Portuguese title"] + "\n"
        s += bold("Título original: ") + m["Original title"] + "\n"
        s += bold("Elenco: ") + m["Cast"] + "\n"
        s += bold("Produtor: ") + m["Producer"] + "\n"
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

def releases(idChat, content):
    send_msg(idChat, 'As próximas estreias dos cinemas NOS são:')

    for m in content:
        s = bold("Título: ") + m["Original title"] + "\n"
        s += bold("Elenco: ") + m["Cast"] + "\n"
        s += bold("Género: ") + m["Genre"] + "\n"
        photo = m["Banner"]
        
        msg = json.dumps({
            'photo': photo,
            'caption': s
        })
        send_photo(idChat, msg)

def movie_details(idChat, content):
    m = content[0]

    s = bold("Título: ") + m["Portuguese title"] + "\n"
    s += bold("Título original: ") + m["Original title"] + "\n"
    s += bold("Elenco: ") + m["Cast"] + "\n"
    s += bold("Produtor: ") + m["Producer"] + "\n"
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

def sessions_by_duration(idChat, content):
    for c in content:
        send_msg(idChat, 'Próximas sessões no ' + c + ':')

        for m in content[c]:
            s = bold("Filme: ") + m["Movie"] + "\n"
            s += bold("Data: ") + m["Start date"] + "\n"
            s += bold("Hora de início: ") + m["Start time"] + "\n"
            s += bold("Duração: ") + str(m["Length (min)"]) + " minutos\n"
            s += bold("Lugares disponíveis: ") + m["Availability"] + "\n"
            s += bold("Link de compra: ") + m["Ticket link"] + "\n"
            send_msg(idChat, s)

def next_sessions(idChat, content):
    for c in content:
        send_msg(idChat, 'Próximas sessões no ' + c + ':')

        for m in content[c]:
            s = bold("Filme: ") + m["Movie"] + "\n"
            s += bold("Data: ") + m["Start date"] + "\n"
            s += bold("Hora de início: ") + m["Start time"] + "\n"
            s += bold("Lugares disponíveis: ") + m["Availability"] + "\n"
            s += bold("Link de compra: ") + m["Ticket link"] + "\n"
            send_msg(idChat, s)

def sessions_by_movie(idChat, content):
    for c in content:
        for m in content[c]:
            send_msg(idChat, 'Próximas sessões do filme "' + m + '" no ' + c + ':')
            for s in content[c][m]:
                st = bold("Data: ") + s["Start date"] + "\n"
                st += bold("Hora de início: ") + s["Start time"] + "\n"
                st += bold("Lugares disponíveis: ") + s["Availability"] + "\n"
                st += bold("Link de compra: ") + s["Ticket link"] + "\n"
                send_msg(idChat, st)

def sessions_by_date(idChat, content):
    for c in content:
        send_msg(idChat, 'Próximas sessões no ' + c + ':')

        for m in content[c]:
            s = bold("Filme: ") + m["Movie"] + "\n"
            s += bold("Data: ") + m["Start date"] + "\n"
            s += bold("Hora de início: ") + m["Start time"] + "\n"
            s += bold("Lugares disponíveis: ") + m["Availability"] + "\n"
            s += bold("Link de compra: ") + m["Ticket link"] + "\n"
            send_msg(idChat, s)

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
    ret = None

    if isinstance(content, str):
        send_msg(idChat, content)
    elif isinstance(content, list) and not allInfo:
        func = switcher.get(cat, send_msg)
        func(idChat, content[0:5])
        send_msg(idChat, "Se pretender ver o resto das opções escreva 'ver mais'.")
    else:
        func = switcher.get(cat, send_msg)
        func(idChat, content)
