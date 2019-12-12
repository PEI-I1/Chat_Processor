from utils import send_msg

def bold(text):
    return "<b>" + text + "</b>"

def linhas_apoio(idChat, content):
    s = 'As linhas de apoio da NOS são:\n'
    s += "\n".join(map(lambda l: bold(l["categoria"] + ": ") + l["numero"], content))
    send_msg(idChat, s)

def phones_search(idChat, content):
    s = 'Os telemóveis que correspondem à procura são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def top_phones(idChat, content):
    s = 'Os top telemóveis são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def promo_phones(idChat, content):
    s = 'Os telemóveis em promoção são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def new_phones(idChat, content):
    s = 'Os novos telemóveis são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def ofer_phones(idChat, content):
    s = 'Os telemóveis com ofertas são: '
    s += "\n".join(map(lambda t: bold(t["nome"] + ": ") + "\n" + bold("Preço: " + t["preco"] + " €\n" + bold("Oferta: ") + t["oferta"] + "\n", content))
    send_msg(idChat, s)

def prest_phones(idChat, content):
    s = 'Os telemóveis que podem ser comprados às prestações são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def points_phones(idChat, content):
    s = 'Os telemóveis que podem ser comprados com pontos são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def phones_price(idChat, content):
    s = 'Os telemóveis entre esses valores são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def phones_brand_price(idChat, content):
    s = 'Os telemóveis da marca entre esses valores são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def phones_brand_promo(idChat, content):
    s = 'Os telemóveis da marca em promoção são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def phones_promo_price(idChat, content):
    s = 'Os telemóveis em promoção entre esses valores são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
    send_msg(idChat, s)

def new_phones_brand(idChat, content):
    s = 'Os novos telemóveis da marca são: '
    s += "\n".join(map(lambda t: bold(t["nome"]) + " com o preço de " + t["preco"] + " €", content))
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
        s += m["Banner"]
        send_msg(idChat, s)

def releases(idChat, content):
    send_msg(idChat, 'As próximas estreias dos cinemas NOS são:')

    for m in content:
        s = bold("Título: ") + m["Original title"] + "\n"
        s += bold("Elenco: ") + m["Cast"] + "\n"
        s += bold("Género: ") + m["Genre"] + "\n"
        s += m["Banner"]
        send_msg(idChat, s)

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
    s += m["Banner"]

    send_msg(idChat, s)

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
    '/fs_scrapper/brand_phones': phones_search,
    '/fs_scrapper/top_phones': top_phones,
    '/fs_scrapper/promo_phones': promo_phones,
    '/fs_scrapper/new_phones': new_phones,
    '/fs_scrapper/ofer_phones': ofer_phones,
    '/fs_scrapper/prest_phones': prest_phones,
    '/fs_scrapper/points_phones': points_phones,
    '/fs_scrapper/phones_price': phones_price,
    '/fs_scrapper/phones_brand_price': phones_brand_price,
    '/fs_scrapper/phones_brand_promo': phones_brand_promo,
    '/fs_scrapper/phones_promo_price': phones_promo_price,
    '/fs_scrapper/new_phones_brand': new_phones_brand,
    '/fs_scrapper/all_wtf': send_msg,
    '/fs_scrapper/wtf_name': send_msg,
    '/fs_scrapper/stores_zone': send_msg,
    '/fs_scrapper/store_address': send_msg,
    '/fs_scrapper/specific_package': send_msg,
    '/fs_scrapper/packages': send_msg,
    '/fs_scrapper/fiber_packages': send_msg,
    '/fs_scrapper/satelite_packages': send_msg,
    '/fs_scrapper/packages_service': send_msg,
    '/fs_scrapper/packages_price': send_msg,
    '/fs_scrapper/packages_service_price': send_msg,
    '/fs_scrapper/fiber_packages_price': send_msg,
    '/fs_scrapper/satelite_packages_price': send_msg,
    '/fs_scrapper/fiber_packages_service': send_msg,
    '/fs_scrapper/satelite_packages_service': send_msg,
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
