import re, os
from utils import clean_msg, get_content
from functools import partial
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

subjects = []
tariffs = []
packages = []
phone_models = []
phone_brands = []
municipies = []
movies = []
packages_types =  ["Pacotes Fibra", "Pacotes Satélite"]
packages_services = ["VOZ", "TV", "NET", "TV+NET", "TV+VOZ", "NET+VOZ", "TV+NET+VOZ"]
movies_genres = ["Ação", "Aventura", "Cinema de arte", "Chanchada", "Comédia", "Comédia romântica", "Comédia dramática", "Comédia de ação", "Dança", "Documentário", "Docuficção", "Drama", "Espionagem", "Escolar", "Faroeste", "Western", "Fantasia científica", "Ficção científica", "Filmes de guerra", "Fantasia", "Guerra", "Musical", "Filme policial", "Romance", "Seriado", "Suspense", "Terror"]
address_starts_with = ["Alameda", "Azinhaga", "Calçada", "Caminho", "Estrada", "Calçadinha", "Rua", "Avenida", "Travessa", "Praça", "Largo", "Praceta", "Beco", "Marquês", "Parque", "Pátio", "Rotunda"]

def update():
    global subjects, tariffs, packages, phone_models, phone_brands, municipies, movies

    aux = get_content("/fs_scrapper/linhas_apoio", [], {})
    subjects = list(map(lambda l: l["categoria"], aux)) if aux != None else aux

    #TODO: add NOS tariffs
    aux = get_content("/fs_scrapper/all_wtf", [], {})
    tariffs = list(map(lambda t: t["nome"], aux)) if aux != None else aux

    aux = get_content("/fs_scrapper/packages", [], {})
    packages = list(map(lambda p: p["nome"], aux)) if aux != None else aux

    aux = get_content("/fs_scrapper/phones_price", ["0.0","1000000.0"], {})
    aux = list(map(lambda p: p["nome"], aux)) if aux != None else aux

    brands = set()
    models = set()
    for p in aux:
        words = p.split()
        brands.add(words[0])
        l = len(words)
        while l > 1:
            models.add(" ".join(words[1:l]))
            models.add(" ".join(words[0:l]))
            l -= 1

    models = filter(lambda m: not re.search(r'^[0-9]+$', m), models)

    phone_brands = list(brands)
    phone_models = list(models)

    with open(os.path.dirname(os.path.abspath(__file__)) + '/../municipios_pt.txt') as f:
        aux = f.readlines()
    municipies = [x.strip() for x in aux]

    #TODO: movies

def init_ner_regex():
    #Atualiza ao iniciar
    update()
    #Depois atualiza de x em x tempo
    scheduler = BackgroundScheduler()
    scheduler.start()
    job = scheduler.add_job(update, IntervalTrigger(hours=1), [])
    atexit.register(scheduler.shutdown)

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
            ents.append({'entity': ad.group(0), 'type': 'FAC'})

    return ents

detect_functions = [
    partial(detect, subjects, 'SUBJECT'),
    partial(detect, tariffs, 'TARIFF'),
    partial(detect, packages_types, 'PACKAGE_TYPE'),
    partial(detect, packages_services, 'PACKAGE_SERVICE'),
    partial(detect, movies_genres, 'MOVIE_GENRE'),
    detect_address,
    partial(detect, phone_brands, 'ORG'),
    partial(detect, phone_models, 'PRODUCT'),
    partial(detect, municipies, 'GPE'),
    partial(detect, movies, 'WORK OF ART')
]
def detect_entities_regex(msg):
    entities = []

    msg = clean_msg(msg)
    for f in detect_functions:
        entities = entities + f(msg)

    return entities
