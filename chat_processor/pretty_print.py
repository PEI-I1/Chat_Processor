from utils import send_msg, send_photo
import json, re

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
    s = 'Os top telemóveis são:\n'
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
    s += "\n".join(map(lambda t: bold(t["nome"] + ": ") + "\n" + bold("Preço: " + t["preco"] + " €\n" + bold("Oferta: ") + t["oferta"] + "\n", content)))
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

def all_wtf(idChat, content):
    s = 'Os pacotes WTF existentes são os seguintes: '
    s += "\n".join(map(lambda p: bold(p["nome"]) + " com o preço de " + p["preco"] + " €", content))
    send_msg(idChat, s)

def wtf_name(idChat, content):
    s = bold("Nome: ") + content["nome"] + "\n"
    s += bold("Preço: ") + content["preco"] + "\n"
    s += bold("Preço/mês: ") + content["preco"] + " €\n"
    s += bold("Net: ") + content["net"] + "\n"
    s += bold("SMS: ") + content["sms"] + "\n"
    s += bold("Chamadas: ") + content["minutos"] + "\n"
    s += bold("Cinemas: ") + content["cinema"] + "\n"
    s += bold("Uber: ") + content["uber"] + "\n"
    s += bold("Uber Eats: ") + content["uber_eats"]
    send_msg(idChat, s)

def stores(idChat, content):
    for l in content:
        s = bold("Nome: ") + l["nome"] + "\n"
        s += bold("Morada: ") + l["morada"] + "\n"
        h = re.split("(.*?\d{2}h\d{2} - \d{2}h\d{2})", l["horario"])
        h = list(filter(None, h))
        s += bold("Horário: ") + "\n               ".join(h)
        send_msg(idChat, s)

def store_address(idChat, content):
    s = bold("Nome: ") + content["nome"] + "\n"
    s += bold("Morada: ") + content["morada"] + "\n"
    h = re.split("(.*?\d{2}h\d{2} - \d{2}h\d{2})", l["horario"])
    h = list(filter(None, h))
    s += bold("Horário: ") + "\n               ".join(h) + "\n"
    s += bold("Serviços: ") + "\n                ".join(content["servicos"])
    send_msg(idChat, s)

def package(idChat, content):
    s = bold("Nome: ") + content["nome"] + "\n"
    s += bold("Tipo: ") + content["Tipo"] + "\n"
    if content["canais"]:
        s += bold("Canais: ") + content["canais"] + "\n"
    if content["net"]:
        s += bold("Net: ") + content["net"] + "\n"
    if content["phone"]:
        s += bold("Telefone: ") + content["phone"] + "\n"
    if content["mobile"]:
        s += bold("Telemóvel: ") + content["mobile"] + "\n"
    if content["netMovel"]:
        s += bold("Net Móvel: ") + content["netMovel"] + "\n"
    send_msg(idChat, s)

    fids = ["Fidelizacao_24Meses", "Fidelizacao_12Meses", "Fidelizacao_6Meses"]
    for fid in fids:
        aux = content[fid]

        s = "Com " + bold(aux["Fidelizacao"]) + " de fidelização:\n"
        s += bold("Preço: ") + aux["preco"] + " €\n"
        s += bold("Preço de Adesão: ") + aux["precoAdesao"] + " €\n"
        s += bold("Vantagens:\n") + "\n".join(aux["vantagens"])
        send_msg(idChat, s)

    aux = content["Sem_Fidelizacao"]

    s = "Sem fidelização:\n"
    s += bold("Preço: ") + aux["preco"] + " €\n"
    s += bold("Preço de Adesão: ") + aux["precoAdesao"] + " €\n"
    s += bold("Vantagens:\n") + "\n".join(aux["vantagens"])
    send_msg(idChat, s)

def packages(idChat, content):
    send_msg(idChat, "Os pacotes NOS disponíveis são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + "\n"
        s += bold("Tipo: ") + content["Tipo"] + "\n"
        s += bold("Serviço: ") + content["servico"]
        send_msg(idChat, s)

def fiber_packages(idChat, content):
    send_msg(idChat, "Os pacotes Fibra da NOS disponíveis são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + "\n"
        s += bold("Serviço: ") + content["servico"]
        send_msg(idChat, s)

def satelite_packages(idChat, content):
    send_msg(idChat, "Os pacotes Satélite da NOS disponíveis são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + "\n"
        s += bold("Serviço: ") + content["servico"]
        send_msg(idChat, s)

def packages_service(idChat, content):
    send_msg(idChat, "Os pacotes NOS com esse serviço são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + "\n"
        s += bold("Tipo: ") + content["Tipo"]
        send_msg(idChat, s)

def packages_price(idChat, content):
    send_msg(idChat, "Os pacotes NOS disponíveis entre esses valores são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + "\n"
        s += bold("Tipo: ") + content["Tipo"] + "\n"
        s += bold("Serviço: ") + content["servico"]
        send_msg(idChat, s)

def packages_service_price(idChat, content):
    send_msg(idChat, "Os pacotes NOS com esse serviço entre esses valores são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + "\n"
        s += bold("Tipo: ") + content["Tipo"]
        send_msg(idChat, s)

def fiber_packages_price(idChat, content):
    send_msg(idChat, "Os pacotes Fibra da NOS disponíveis entre esses valores são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + "\n"
        s += bold("Serviço: ") + content["servico"]
        send_msg(idChat, s)

def satelite_packages_price(idChat, content):
    send_msg(idChat, "Os pacotes Satélite da NOS disponíveis entre esses valores são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"] + "\n"
        s += bold("Serviço: ") + content["servico"]
        send_msg(idChat, s)

def fiber_packages_service(idChat, content):
    send_msg(idChat, "Os pacotes Fibra da NOS com esse serviço são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"]
        send_msg(idChat, s)

def satelite_packages_service(idChat, content):
    send_msg(idChat, "Os pacotes Satélite da NOS com esse serviço são os seguintes:")

    for p in content:
        s = bold("Nome: ") + content["nome"] + "\n"
        s += bold("Preço: ") + content["preco"]
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
    '/fs_scrapper/all_wtf': all_wtf,
    '/fs_scrapper/wtf_name': wtf_name,
    '/fs_scrapper/stores': stores,
    '/fs_scrapper/store_address': store_address,
    '/fs_scrapper/specific_package': package,
    '/fs_scrapper/packages': packages,
    '/fs_scrapper/fiber_packages': fiber_packages,
    '/fs_scrapper/satelite_packages': satelite_packages,
    '/fs_scrapper/packages_service': packages_service,
    '/fs_scrapper/packages_price': packages_price,
    '/fs_scrapper/packages_service_price': packages_service_price,
    '/fs_scrapper/fiber_packages_price': fiber_packages_price,
    '/fs_scrapper/satelite_packages_price': satelite_packages_price,
    '/fs_scrapper/fiber_packages_service': fiber_packages_service,
    '/fs_scrapper/satelite_packages_service': satelite_packages_service,
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
