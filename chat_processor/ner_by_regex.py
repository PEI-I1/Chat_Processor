import os, nltk
import regex as re
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
packages_types =  ["Pacotes Fibra", "Pacotes Satélite", "Fibra", "Satélite"]
packages_services = ["VOZ", "TV", "NET", "TV+NET", "TV+VOZ", "NET+VOZ", "TV+NET+VOZ"]
movies_genres = ["Ação", "Aventura", "Cinema de arte", "Chanchada", "Comédia", "Comédia romântica", "Comédia dramática", "Comédia de ação", "Dança", "Documentário", "Docuficção", "Drama", "Espionagem", "Escolar", "Faroeste", "Western", "Fantasia científica", "Ficção científica", "Filmes de guerra", "Fantasia", "Guerra", "Musical", "Filme policial", "Romance", "Seriado", "Suspense", "Terror"]
address_starts_with = ["Al\.", "Alameda", "Az\.", "Azinhaga", "Cc.", "Calçada", "Cam\.", "Caminho", "Estr.", "Estrada", "Ccnh\.", "Calçadinha", "R\.", "Rua", "Av\.", "Avenida", "Tv\.", "Travessa", "Pc\.", "Praça", "Lg\.", "Largo", "Pct\.", "Praceta", "Bc\.", "Beco", "Mq\.", "Marquês", "Pq\.", "Parque", "Pto\.", "Pátio", "Rot\.", "Rotunda", "Qta\.", "Quinta"]
detect_functions = []
phones_booleans = [("sim", "Sim"), ("nao", "Não"), (r"promo(cao|coes)?", "promo"), ("novos?", "new"), ("recentes?", "new"), ("descontos?", "promo"), ("ofertas?", "ofer"), ("prestac(ao|oes)", "prest"), ("pontos?", "points")]

def update():
    global subjects, tariffs, packages, phone_models, phone_brands, municipies, movies, detect_functions

    aux = get_content("/fs_scrapper/linhas_apoio", [], {})
    subs = set()
    if aux:
        for s in aux:
            subs.add(s["categoria"])
            words = s["categoria"].split()
            for w in words:
                wl = w.lower()
                if w not in nltk.corpus.stopwords.words('portuguese') and not re.match('\p{punct}', w) and wl != "apoio":
                    subs.add(w.title())
    subjects = list(subs)

    #TODO: add NOS tariffs
    aux = get_content("/fs_scrapper/wtf", [], {})
    tariffs = list(map(lambda t: t["nome"], aux)) if aux != None else aux

    aux = get_content("/fs_scrapper/packages", [], {})
    packages = list(set(map(lambda p: p["nome"], aux))) if aux != None else aux

    aux = get_content("/fs_scrapper/phones", [], {"min": "0", "max": "10000000"})
    aux = list(map(lambda p: p["nome"], aux)) if aux != None else aux

    brands = set()
    models = set()
    if aux:
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
    movie_info = get_content("/scrapper/movies/search", [], {"synopsis": " "})
    #movie_titles = list(map(lambda p: p["Portuguese title"], release_info)) if release_info else release_info
    movies = extract_and_flatten(movie_info, ["Portuguese title", "Original title"])
    
    detect_functions = [
        partial(detect, subjects, 'SUBJECT'),
        partial(detect, tariffs, 'TARIFF'),
        partial(detect, packages, 'PACKAGE'),
        partial(detect, packages_types, 'PACKAGE_TYPE'),
        partial(detect, packages_services, 'PACKAGE_SERVICE'),
        partial(detect, movies_genres, 'MOVIE_GENRE'),
        partial(detect, phone_brands, 'ORG'),
        partial(detect, phone_models, 'PRODUCT'),
        partial(detect, municipies, 'GPE'),
        partial(detect, movies, 'WORK OF ART'),
        detect_phones_boolean
    ]

def extract_and_flatten(src, poi):
    ''' Extract all relevant information from each item in source
    and flatten result
    :param: source dictionary
    :param: parameters of interest
    :return: flat list
    '''
    ufl = list(map(lambda p: [p[spoi] for spoi in poi], src)) if src else src
    fl = [item for inner_list in ufl for item in inner_list]
    return fl

    
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
        ad = re.search(r'^(\s*' + a + r'.*)$', msg, re.IGNORECASE)
        if ad:
            ents.append({'entity': ad.group(1), 'type': 'FAC'})

    return ents

def detect_phones_boolean(msg):
    ents = []
    
    for (rg, v) in phones_booleans:
        pb = re.search(r'^\s*' + rg + r'.*$', msg)
        if pb:
            ents.append({'entity': v, 'type': 'PHONES_BOOLEAN'})

    return ents

def detect_entities_regex(msg):
    entities = detect_address(msg)

    msg = clean_msg(msg)
    for f in detect_functions:
        entities = entities + f(msg)

    return entities
