from utils import send_msg

def bold(text):
    return "<b>" + text + "</b>"

def releases(idChat, content):
    send_msg(idChat, 'As próximas estreias dos cinemas NOS são:')

    for m in content:
        s = bold("Título: ") + m["Original title"] + "\n"
        s += bold("Elenco: ") + m["Cast"] + "\n"
        s += bold("Género: ") + m["Genre"] + "\n"
        s += m["Banner"]
        send_msg(idChat, s)

switcher = {
    '/fs_scrapper/linhas_apoio': send_msg,
    '/fs_scrapper/phone_model': send_msg,
    '/fs_scrapper/brand_phones': send_msg,
    '/fs_scrapper/top_phones': send_msg,
    '/fs_scrapper/promo_phones': send_msg,
    '/fs_scrapper/new_phones': send_msg,
    '/fs_scrapper/ofer_phones': send_msg,
    '/fs_scrapper/prest_phones': send_msg,
    '/fs_scrapper/points_phones': send_msg,
    '/fs_scrapper/phones_price': send_msg,
    '/fs_scrapper/phones_brand_price': send_msg,
    '/fs_scrapper/phones_brand_promo': send_msg,
    '/fs_scrapper/phones_promo_price': send_msg,
    '/fs_scrapper/new_phones_brand': send_msg,
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
    '/scrapper/cinemas/search': send_msg,
    '/scrapper/movies/by_cinema': send_msg,
    '/scrapper/movies/search': send_msg,
    '/scrapper/movies/releases': releases,
    '/scrapper/movies/details': send_msg,
    '/scrapper/sessions/by_duration': send_msg,
    '/scrapper/sessions/next_sessions': send_msg,
    '/scrapper/sessions/by_movie': send_msg,
    '/scrapper/sessions/by_date': send_msg
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
