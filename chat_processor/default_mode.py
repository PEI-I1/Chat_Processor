from categoria_dic import cat as dicionario
from spell_checker import spell_check_ss
from utils import process_list, get_params, get_content 
import globals, nltk, json
import regex as re

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

def get_response_default(idChat, idUser, msg, name):
    cat, confianca = get_categoria_frase(msg)
    params = proc_ents(globals.ner_model([msg]))

    if confianca > 0.65:
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

                content = get_content(cat, [], {})
                #perceber se o pedido deu ou não erro
                #se der erro devolver uma mensagem de erro
            else:
                #perguntar ao utilizador os parâmetros
                print()
        else:
            content = get_content(cat, [], {})

        #se for uma lista devolve de forma diferente
        if isinstance(content, list):
            msg_send = process_list(content)
            globals.redis_db.set("vermais" + idChat, json.dumps(content))
        else:
            msg_send = content
    else:
        msg_send = "Desculpe mas não foi possível identificar o que pretende. Tente de novo!"
    return str(msg_send)
