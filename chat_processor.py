#!/usr/bin/env python3

import os
from spell_checker import spell_check_google, spell_check_psc
import regex as re
from categoria_dic import cat as dicionario
import requests
from cacheout import Cache

import nltk
nltk_dir = os.path.dirname(os.path.abspath(__file__)) + '/nltk_data'
nltk.data.path.append(nltk_dir)

cache = None

def init():
    global cache
    cache = Cache(maxsize=4096, ttl=0, default=None)
    download_recursos()

def download_recursos():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', download_dir=nltk_dir)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', download_dir=nltk_dir)

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
            assoc_words = dicionario[cat]
            for word in dicionario[cat]:
                if word == pal:
                    noccur[cat] = noccur.get(cat, 0) + 1
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
    inp = spell_check_google(inp)
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

def get_response(idChat, idUser, msg, name):
    if msg.lower() == "ver mais":
        content = cache.get("vermais" + idChat)
        cache.delete("vermais" + idChat)
        msg_send = process_all_list(content)
    else:
        cat, confianca = get_categoria_frase(msg)

        if confianca > 0.65:
            if cat == "resolucao_problemas":
                #criar um fluxo diferente para a resolução de problemas
                #por exemplo ir perguntando parametros que são necessários inserir no modelo e que ainda não temos, seja pelo contexto da conversa seja pelo utilizador
                #tb deve ser necessário fazer aqui a autenticação
            else:

                if has_params(cat):
                    #TODO: obter parametros da frase
                    content = get_content(cat) #adicionar parametros)
                    #perceber se o pedido deu ou não erro
                    #se der erro devolver uma mensagem de erro
                else:
                    content = get_content(cat)

                #se for uma lista devolve de forma diferente
                if isinstance(content, list):
                    msg_send = process_list(content)
                    cache.set("vermais" + idChat, content)
                else:
                    msg_send = content
        else:
            msg_send = "Desculpe mas não foi possível identificar o que pretende. Tente de novo!"
    return str(msg_send)

def get_content(pedido):
    '''recebe um pedido e retorna a informação '''
    URL = 'http://127.0.0.1:5000/'
    try:
        res = requests.get(URL + pedido).json().get('response')
        res.raise_for_status()
    except e:
        res = None
    return res

##################################### TESTING ####################################
# test pyspellchecker
#print(spell_check_psc(['como', 'fazer', 'arros']))
