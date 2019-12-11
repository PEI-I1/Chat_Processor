def bold(text):
    return "<b>" + text + "</b>"

def releases(content):
    s = 'As próximas estreias dos cinemas NOS são:\n'

    #s += "<ul>\n"

    for m in content:
        #s += "<li>\n"
        s += "\n\n"
        s += bold("Título: ") + m["Original title"] + "\n"
        s += bold("Elenco: ") + m["Cast"] + "\n"
        s += bold("Género: ") + m["Genre"] + "\n"
        s += m["Banner"] + "\n"
        #s += "</li>\n"

    #s += "</ul>"
    return s

switcher = {
    '/fs_scrapper/linhas_apoio': str,
    '/fs_scrapper/phone_model': str,
    '/fs_scrapper/brand_phones': str,
    '/fs_scrapper/top_phones': str,
    '/fs_scrapper/promo_phones': str,
    '/fs_scrapper/new_phones': str,
    '/fs_scrapper/ofer_phones': str,
    '/fs_scrapper/prest_phones': str,
    '/fs_scrapper/points_phones': str,
    '/fs_scrapper/phones_price': str,
    '/fs_scrapper/phones_brand_price': str,
    '/fs_scrapper/phones_brand_promo': str,
    '/fs_scrapper/phones_promo_price': str,
    '/fs_scrapper/new_phones_brand': str,
    '/fs_scrapper/all_wtf': str,
    '/fs_scrapper/wtf_name': str,
    '/fs_scrapper/stores_zone': str,
    '/fs_scrapper/store_address': str,
    '/fs_scrapper/specific_package': str,
    '/fs_scrapper/packages': str,
    '/fs_scrapper/fiber_packages': str,
    '/fs_scrapper/satelite_packages': str,
    '/fs_scrapper/packages_service': str,
    '/fs_scrapper/packages_price': str,
    '/fs_scrapper/packages_service_price': str,
    '/fs_scrapper/fiber_packages_price': str,
    '/fs_scrapper/satelite_packages_price': str,
    '/fs_scrapper/fiber_packages_service': str,
    '/fs_scrapper/satelite_packages_service': str,
    '/scrapper/cinemas/search': str,
    '/scrapper/movies/by_cinema': str,
    '/scrapper/movies/search': str,
    '/scrapper/movies/releases': releases,
    '/scrapper/movies/details': str,
    '/scrapper/sessions/by_duration': str,
    '/scrapper/sessions/next_sessions': str,
    '/scrapper/sessions/by_movie': str,
    '/scrapper/sessions/by_date': str
}

def pretty_print(cat, content, allInfo):
    ret = None

    if isinstance(content, str):
        ret = content
    elif isinstance(content, list) and not allInfo:
        func = switcher.get(cat, str)
        ret = func(content[0:5])
        ret += "\n\nSe pretender ver o resto das opções escreva 'ver mais'."
    else:
        func = switcher.get(cat, str)
        ret = func(content)

    return ret
