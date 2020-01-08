#!/usr/bin/env python3

from rules_mode import get_response_rules
from default_mode import get_response_default, ntp_answer
from pretty_print import pretty_print, ver_mais, title
from utils import send_msg, clean_msg, send_menu
from ner_by_regex import init_ner_regex
import globals, json, nltk, re

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

def forward_to(idChat, chatData, data):
    '''Forward msg to other component
    :param: idChat
    :param: user chat state
    :param: data to send to user
    '''
    globals.redis_db.set(idChat, json.dumps(chatData))

    if 'menu' in data:
        send_menu(idChat, data['msg'], data['menu'])
    else:
        send_msg(idChat, data['msg'])

def process_content_num(idChat, content, num):
    '''Process choice made by user to filter content
    :param: id chat
    :param: content to filter
    :param: user choice
    '''
    n = 1
    for c in content['value']:
        if n == num:
            title(idChat, content['value'], content['cat'], c)
            ver_mais(idChat)
        n += 1
    if num >= n:
        globals.redis_db.set("content" + str(idChat), json.dumps(content))
        send_msg(idChat, "Desculpe a escolha que inseriu não é uma das hipóteses. Volte a tentar.")

def process_content(idChat, msg, content):
    '''Process content for cases when we want to filter the content
    :param: id chat
    :param: user message
    :param: content to filter
    '''
    globals.redis_db.delete("content" + str(idChat))
    m = clean_msg(msg)
    if not re.search(r'^\s*0\s*$', m) and not re.search(r'\bnenhuma das hipoteses\b', m) and not re.search(r'\bnenhuma?\b', m):
        num = re.search(r'^\s*([0-9]+)\s*$', msg) 
        if num:
            num = num.group(1)
            process_content_num(idChat, content, int(num))
        else:
            i = 0
            n = len(content['keys'])
            found = False
            while i < n and not found:
                if re.search(r'\b' + content['keys'][i]['match'] + r'\b', msg):
                    found = True
                    process_content_num(idChat, content, content['keys'][i]['choice'])
                i += 1
            if not found:
                process_content_num(idChat, content, n+1)
    else:
        send_msg(idChat, "Faça uma nova questão. O que pretende saber?")

def get_response(idChat, idUser, msg, name, location):
    ''' For a given user message answer him
    :param: id chat
    :param: id user
    :param: user message
    :param: user name
    :param: user location
    '''
    contentAux = globals.redis_db.get("content" + str(idChat))
    content = json.loads(contentAux) if contentAux else None

    if content:
        process_content(idChat, msg, content)
    else:
        chatDataAux = globals.redis_db.get(idChat)
        chatData = json.loads(chatDataAux) if chatDataAux else None

        if not chatData:
            chatData = {
                "status": "",
                "tries": 0,
                "cat": "",
                "cat_change": "",
                "cat_change_last_msg": "",
                "paramsStatus": "new",
                "locationParam": None,
                "paramsRequired": {},
                "paramsOptional":{},
                "paramsMissingRequired": {},
                "paramsMissingOptional": {},
                "msg_params": {}
            }

        if location:
            chatData["status"] = ""
            chatData["locationParam"] = location

        if chatData["status"] == "modo regras":
            forward_to(idChat, chatData, get_response_rules(idChat, idUser, msg, name, chatData))
        elif chatData["status"] == "modo problemas":
            globals.redis_db.set(idChat, json.dumps(chatData))
            ntp_answer(idChat, msg)
        else:
            m = clean_msg(msg)
            if re.match(r'\bmodo (de )?regras\b', m):
                chatData["status"] = "modo regras"
                forward_to(idChat, chatData, get_response_rules(idChat, idUser, msg, name, chatData))
            elif re.match(r'\bver mais\b', m):
                ver_mais(idChat)
            else:
                get_response_default(idChat, idUser, msg, name, chatData)
