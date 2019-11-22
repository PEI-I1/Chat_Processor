#!/usr/bin/env python3

from rules_mode import get_response_rules
from default_mode import get_response_default
from utils import process_all_list
from config import urls
import os, logging, json
import nltk, deeppavlov
import redis

ner_model = None
redis_db = None

def init():
    download_recursos()

    #Remove debug do Tensorflow
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"
    logging.getLogger('tensorflow').disabled = True

    #build model para obter entidades
    global ner_model
    ner_model = deeppavlov.build_model(deeppavlov.configs.ner.ner_ontonotes_bert_mult, download=True)

    #Connect to redis
    global redis_db
    redis_db = redis.StrictRedis(host=urls['REDIS']['host'], port=urls['REDIS']['port'], db=0)

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
    if msg.lower() == "ver mais":
        content = json.loads(redis_db.get("vermais" + idChat))
        redis_db.delete("vermais" + idChat)
        return str(process_all_list(content))
    else:
        return get_response_default(idChat, idUser, msg, name)
