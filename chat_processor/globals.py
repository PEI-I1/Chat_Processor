from config import urls
import deeppavlov
import redis

def init():
    '''Init global variables.
    Build deeppavlov model for NER.
    Create a connection to redis.
    '''
    #build model para obter entidades
    global ner_model
    ner_model = deeppavlov.build_model(deeppavlov.configs.ner.ner_ontonotes_bert_mult, download=True)

    #Connect to redis
    global redis_db
    redis_db = redis.StrictRedis(host=urls['REDIS']['host'], port=urls['REDIS']['port'], db=0)
