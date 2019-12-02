#!/usr/bin/env python3

from rules_mode import get_response_rules
from default_mode import get_response_default
from utils import process_all_list
import globals, json, nltk

def init():
    download_recursos()
    globals.init()

def download_recursos():
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

def get_response(idChat, idUser, msg, name):
    chatDataAux = globals.redis_db.get(idChat)
    chatData = json.loads(chatDataAux) if chatDataAux else None

    if not chatData:
        chatData = {"msgs": [], "status": "", "tries": 0,
                    "cat": "", "cat_change": "",
                    "paramsRequired": [], "paramsOptional":[]}
        globals.redis_db.set(idChat, json.dumps(chatData))

    if chatData["status"] == "modo regras":
        return get_response_rules(idChat, idUser, msg, name)
    else:
        m = msg.lower()
        if m == "modo de regras":
            chatData["status"] = "modo regras"
            globals.redis_db.set(idChat, json.dumps(chatData))
            return get_response_rules(idChat, idUser, msg, name)
        elif m == "ver mais":
            content = json.loads(globals.redis_db.get("vermais" + idChat))
            globals.redis_db.delete("vermais" + idChat)
            return str(process_all_list(content))
        else:
            return get_response_default(idChat, idUser, msg, name, chatData)
