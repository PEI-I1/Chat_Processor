import re
from utils import clean_msg
from functools import partial

subjects = []
#TODO: get subjects from FS Scraper
tariffs = []
#TODO: get tariffs from FS Scraper
packages = []
#TODO: get packages from FS Scraper
packages_types =  ["Pacotes Fibra", "Pacotes Satélite"]
packages_services = ["VOZ", "TV", "NET", "TV+NET", "TV+VOZ", "NET+VOZ", "TV+NET+VOZ"]
movies_genres = ["Ação, Aventura, Cinema de arte, Chanchada, Comédia, Comédia romântica, Comédia dramática, Comédia de ação, Dança, Documentário, Docuficção, Drama, Espionagem, Escolar, Faroeste, Western, Fantasia científica, Ficção científica, Filmes de guerra, Fantasia, Guerra, Musical, Filme policial, Romance, Seriado, Suspense, Terror"]
address_starts_with = ["Rua", "Avenida", "Travessia", "Praça", "Largo"]

def detect(words, t, msg):
    ents = []
    
    for w in words:
        if re.search(r'\b' + clean_msg(w) + r'\b', msg):
            ents.append({'entity': w, 'type': t})

    return ents

def detect_address(msg):
    ents = []
    
    for a in address_starts_with:
        ad = re.search(r'^\s*' + clean_msg(a) + r'.*$', msg)
        if ad:
            ents.append({'entity': ad.group(0), 'type': 'ADDRESS'})

    return ents

detect_functions = [
    partial(detect, subjects, 'SUBJECT'),
    partial(detect, tariffs, 'TARIFF'),
    partial(detect, packages_types, 'PACKAGE_TYPE'),
    partial(detect, packages_services, 'PACKAGE_SERVICE'),
    partial(detect, movies_genres, 'MOVIE_GENRE'),
    detect_address
]
def detect_entities_regex(msg):
    entities = []

    msg = clean_msg(msg)
    for f in detect_functions:
        entities = entities + f(msg)

    return entities
