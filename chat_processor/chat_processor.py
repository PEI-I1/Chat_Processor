#!/usr/bin/env python3

from rules_mode import get_response_rules
from default_mode import get_response_default
from pretty_print import pretty_print
from utils import send_msg, clean_msg, send_menu
from ner_by_regex import init_ner_regex
import globals, json, nltk

def init():
    ''' Init. Download necessary resources, init global variables
    (redis connection and deeppavlov model) and init NER by regex.
    '''
    download_recursos()
    globals.init()
    init_ner_regex()

def download_recursos():
    ''' Download necessary resources for NLTK
    '''
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    ## required for deeppavlov package
    try:
        nltk.data.find('misc/perluniprops')
    except LookupError:
        nltk.download('perluniprops', quiet=True)
    try:
        nltk.data.find('corpora/nonbreaking_prefixes')
    except LookupError:
        nltk.download('nonbreaking_prefixes', quiet=True)

def ver_mais(idChat):
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
        send_msg(idChat, "Não existe lista para ver...")

def forward_to(idChat, chatData, data):
    globals.redis_db.set(idChat, json.dumps(chatData))

    if isinstance(data, str):
        send_msg(idChat, data)
    else:
        send_menu(idChat, data['msg'], data['menu'])

def get_response(idChat, idUser, msg, name, location):
    ''' For a given user message answer him
    :param: id chat
    :param: id user
    :param: user message
    :param: user name
    :param: user location
    '''
    chatDataAux = globals.redis_db.get(idChat)
    chatData = json.loads(chatDataAux) if chatDataAux else None

    if not chatData:
        chatData = {"msgs": [], "status": "", "tries": 0,
                    "cat": "", "cat_change": "", "cat_change_last_msg": "",
                    "paramsStatus": "new", "locationParam": None,
                    "paramsRequired": {}, "paramsOptional":{},
                    "paramsMissingRequired": {}, "paramsMissingOptional": {}}

    if location:
        chatData["status"] = ""
        chatData["locationParam"] = location

    if chatData["status"] == "modo regras":
        forward_to(idChat, chatData, get_response_rules(idChat, idUser, msg, name, chatData))
    elif chatData["status"] == "modo problemas":
        forward_to(idChat, chatData, get_solver(idChat, msg))
    else:
        m = clean_msg(msg)
        if m == "modo de regras":
            chatData["status"] = "modo regras"
            forward_to(idChat, chatData, get_response_rules(idChat, idUser, msg, name, chatData))
        elif m == "ver mais":
            ver_mais(idChat)
        else:
            get_response_default(idChat, idUser, msg, name, chatData)
