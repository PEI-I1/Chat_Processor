from categoria_dic import cat as dicionario
from spell_checker import spell_check_ss
from utils import *
import globals, nltk, json
import regex as re

confianca_level = 0.70

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

# separa a lista de tuplos de (tipo:entidade) em duas listas de tuplos
# com os params válidos e os params para serem perguntados
def separate_params(tuplo_params):
    valid_params = []
    params_to_ask = []

    for tipo,entidade in tuplo_params:
        if entidade:
            valid_params.append(tuple((tipo,entidade)))
        else:
            params_to_ask.append(tuple((tipo,entidade)))

    return valid_params, params_to_ask

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

# compara os params obrigatórios da frase (params) com os da dic (cat_params)
def compare_required_params(params, cat_params):
    to_ask = []
    valid = []
    tuplo_params = []

    for p in cat_params:
        found = None
        for pp in params:
            # TODO adicionar situação com tipos de entidades repetidos (intervalo de tempo ou dinheiro)
            if pp.type == p:
                found = tuple((p,pp.entity))

        if found == None:
            found = tuple((p,None))

        tuplo_params.append(found)

    return tuplo_params

def process_params(idChat, idUser, msg, name, chatData):
    if len(cat_params) > 0:
        tuplo_params = compare_required_params(params, cat_params)

        #TODO esta função
        tuplo_params = compare_required_params(params, cat_params)
        valid_params, params_to_ask = separate_params(tuplo_params)

        if len(params_to_ask) == 0:
            # alterar o valid params de forma a que o get_content consiga ler
            content = get_content(cat,valid_params,{})
            globals.redis_db.delete(idChat)
            # plen = len(valid_params)
            # if plen == 1:
            #     cat += '/' + urllib.parse.quote(params_to_ask[0], safe='')
            # elif plen == 2:
            #     if params_to_ask[0] < params_to_ask[1]:
            #         cat += '/' + urllib.parse.quote(params_to_ask[0] + '/' + params_to_ask[1])
            #     else:
            #         cat += '/' + urllib.parse.quote(params_to_ask[1] + '/' + params_to_ask[0])
            # else:
            #     #TODO
            #     #guardar contexto para quando o utilizador responder
            #     #perguntar ao utilizador um dos parametros que falta
            #     #se ao fim de 5 vezes o utilizador n responder corretamente, se for possivel devolver a cat sem parametros (verificar canRequestWithoutParams) senão dizer para ligar para o apoio (se possivel restringindo o assunto, senão devolvendo a lista)
            #     print()

            content = get_content(cat, [], {})\
            #perceber se o pedido deu ou não erro
            #se der erro devolver uma mensagem de erro
        else:
            #perguntar ao utilizador os parâmetros
            content = get_phrase_missing_param(cat)
    else:
        # NOTE: guardar é inutil neste caso, pralem de seguir o diagrama
        # globals.redis_db.set(idChat, "algo")
        content = get_content(cat, [], {})
        globals.redis_db.delete(idChat)

    #se for uma lista devolve de forma diferente
    if isinstance(content, list):
        msg_send = process_list(content)
        globals.redis_db.set("vermais" + idChat, json.dumps(content))
    else:
        msg_send = content

    return msg_send

def get_response_default(idChat, idUser, msg, name, chatData):
    #Mudar categoria???
    if chatData["status"] == "mudar categoria?":
        mc = clean_msg(msg)

        if mc == "sim":
            chatData["cat"] = chatData["cat_change"]
            chatData["cat_change"] = ""
            globals.redis_db.set(idChat, json.dumps(chatData))

        msg_send = process_params(idChat, idUser, msg, name, chatData)
    else:
        cat, confianca = get_categoria_frase(msg)
        params = proc_ents(globals.ner_model([msg]))

        if chatData["cat"] == "":
            if confianca > confianca_level:
                chatData["cat"] == cat
                globals.redis_db.set(idChat, json.dumps(chatData))
                msg_send = process_params(idChat, idUser, msg, name, chatData)
            else:
                if chatData["tries"] == 5:
                    msg_send = "Desculpe mas não foi possível identificar o que pretende.\n\n"
                    msg_send += "Pode tentar o modo de regras ao escrever 'modo de regras'.\n\n"
                    msg_send += "Ou pode se quiser ligar para uma das seguintes linhas de apoio:\n"
                    #TODO: tentar melhorar as linhas de apoio por forma a tentar mostrar apenas o de um assunto
                    msg_send += process_all_list(get_content("linhas_apoio", [], {}))
                    globals.redis_db.delete(idChat)
                else:
                    chatData["tries"] += 1
                    globals.redis_db.set(idChat, json.dumps(chatData))
                    msg_send = "Desculpe mas não foi possível identificar o que pretende. Tente de novo!"
        else:
            if confianca > confianca_level:
                if chatData["cat"] == cat:
                    msg_send = process_params(idChat, idUser, msg, name, chatData)
                else:
                    chatData["cat_change"] = cat
                    chatData["params"] = params
                    globals.redis_db.set(idChat, json.dumps(chatData))
                    msg_send = "Pretende mudar de categoria de '" + chatData["cat"] + "' para '" + cat + "'? Responda por favor 'sim' ou 'não'"
            else:
                msg_send = process_params(idChat, idUser, msg, name, chatData)

    return str(msg_send)
