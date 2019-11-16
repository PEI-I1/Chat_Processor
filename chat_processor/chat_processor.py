#!/usr/bin/env python3

import os
from spell_checker import spell_check_google, spell_check_ss
import regex as re
from categoria_dic import cat as dicionario
import requests
from cacheout import Cache
from config import urls 
import nltk
import deeppavlov
import urllib.parse

cache = None
ner_model = None

def init():
    global cache
    cache = Cache(maxsize=4096, ttl=0, default=None)

    nltk_dir = os.path.dirname(os.path.abspath(__file__)) + '/nltk_data'
    nltk.data.path.append(nltk_dir)
    download_recursos()

    #Remove debug do Tensorflow
    import logging
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"
    logging.getLogger('tensorflow').disabled = True

    #build model para obter entidades
    global ner_model
    ner_model = deeppavlov.build_model(deeppavlov.configs.ner.ner_ontonotes_bert_mult, download=True)

def download_recursos():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', download_dir=nltk_dir, quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', download_dir=nltk_dir, quiet=True)

# remove stopwords e pontuação da mensagem recebida como input
# retorna uma lista com as palavras
def limpa_texto(mensagem):
    mensagem = nltk.word_tokenize(mensagem.lower())
    mensagem = [palavra for palavra in mensagem if palavra not in nltk.corpus.stopwords.words('portuguese') and not re.match('\p{punct}', palavra)]
    return mensagem

# cria um dic 'noccur' com o número de occorências na frase para cada categoria
def criar_noccur_dic(palavras):
    noccur = {}
    for pal in palavras:
        for cat in dicionario: 
            for word in cat['words']:
                if word == pal:
                    noccur[cat['request']] = noccur.get(cat['request'], 0) + 1
    return noccur

# com base na dic do noccur calcular qual é a categoria mais provável e a sua confiança
# confiança = noccur da categoria que aparece mais / número de ocorrência de todas as categorias
def calcula_confianca(noccur):
    total = 0
    confianca = 0
    if len(noccur):
        cat_maior = max(noccur, key=noccur.get)
        valor_cat = noccur.get(cat_maior)

        for valor in noccur.values():
            total += valor

        confianca = valor_cat / total
    else:
        cat_maior = "Not Found"
        confianca = 0
    return cat_maior,confianca
    

def get_categoria_frase(inp):
    inp = spell_check_ss(inp)
    palavras = limpa_texto(inp)
    noccur = criar_noccur_dic(palavras)
    return calcula_confianca(noccur)

def process_list(content):
    n = 0
    size = len(content)
    msg_send = ""

    while n < size and n < 5:
        for key in content[n]:
            msg_send += key + ": " + content[n][key] + "\n"
        n += 1
        msg_send += "\n"

    if n == 5:
        msg_send += "Se pretender ver o resto das opções escreva 'ver mais'."
    return msg_send

def process_all_list(content):
    msg_send = ""

    for elem in content:
        for key in elem:
            msg_send += key + ": " + elem[key] + "\n"
        msg_send += "\n"

    return msg_send

def get_service(cat):
    size = len(dicionario)
    i = 0
    foundCat = None

    while i < size and foundCat == None:
        if dicionario[i]['request'] == cat:
            foundCat = dicionario[i]['service']

    return urls[foundCat]

def get_params(cat):
    size = len(dicionario)
    i = 0
    foundCat = None

    while i < size and foundCat == None:
        if dicionario[i]['request'] == cat:
            foundCat = dicionario[i]['params']

    return foundCat

def proc_ents(inp):
    words = inp[0][0]
    ents = inp[1][0]

    i = 0
    w = ""
    t = ""
    ret = []
    while i < len(words):
        if ents[i] != "O":
            if ents[i][0] == 'B':
                if w != "":
                    ret.append({'entity': w, 'type': t})
                w = words[i]
                t = ents[i][2:]
            else:
                w += " " + words[i]
        i+=1

    if w != "":
        ret.append({'entity': w, 'type': t})

    return ret

def compare_params(params, cat_params):
    to_ask = []
    valid = []

    for p in cat_params:
        found = None
        for pp in params:
            if p.type == pp:
                found = p

        if found == None:
            to_ask.append(p)
        else:
            valid.append(p)

    return valid, to_ask


def get_response(idChat, idUser, msg, name):
    if msg.lower() == "ver mais":
        content = cache.get("vermais" + idChat)
        cache.delete("vermais" + idChat)
        msg_send = process_all_list(content)
    else:
        cat, confianca = get_categoria_frase(msg)
        params = proc_ents(ner_model([msg]))

        if confianca > 0.65:
            #obtém o url de acordo a categoria
            URL = get_service(cat)
            cat_params = get_params(cat)
            if len(cat_params) > 0:
                valid_params, params_to_ask = compare_params(params, cat_params)

                if len(params_to_ask) == 0:
                    plen = len(valid_params)
                    if plen == 1:
                        cat += '/' + urllib.parse.quote(params_to_ask[0], safe='') 
                    elif plen == 2:
                        if params_to_ask[0] < params_to_ask[1]:
                            cat += '/' + urllib.parse.quote(params_to_ask[0] + '/' + params_to_ask[1])
                        else:
                            cat += '/' + urllib.parse.quote(params_to_ask[1] + '/' + params_to_ask[0])
                    else:
                        #TODO
                        #guardar contexto para quando o utilizador responder
                        #perguntar ao utilizador um dos parametros que falta
                        #se ao fim de 5 vezes o utilizador n responder corretamente, se for possivel devolver a cat sem parametros (verificar canRequestWithoutParams) senão dizer para ligar para o apoio (se possivel restringindo o assunto, senão devolvendo a lista)
                        print()

                    content = get_content(URL, cat)
                    #perceber se o pedido deu ou não erro
                    #se der erro devolver uma mensagem de erro
                else:
                    #perguntar ao utilizador os parâmetros
                    print()
            else:
                content = get_content(URL, cat)

            #se for uma lista devolve de forma diferente
            if isinstance(content, list):
                msg_send = process_list(content)
                cache.set("vermais" + idChat, content)
            else:
                msg_send = content
        else:
            msg_send = "Desculpe mas não foi possível identificar o que pretende. Tente de novo!"
    return str(msg_send)

def get_content(URL, pedido):
    '''recebe um pedido e retorna a informação '''
    try:
        res = requests.get(URL + pedido)
        res.raise_for_status()
        res = res.json().get('response')
    except:
        res = None
    return res
