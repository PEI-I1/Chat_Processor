import nltk
import regex as re
from categoria_dic import categoria

# como corrigir erros ortográficos -> usar ngramas?

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
        cat = categoria.get(pal)
        if cat:
            noccur[cat] = noccur.get(cat,0)+1
    return noccur

# com base na dic do noccur calcular qual é a categoria mais provável e a sua confiança
# confiança = noccur da categoria que aparece mais / número de ocorrência de todas as categorias
def calcula_confianca(noccur):
    total = 0
    confianca = 0
    cat_maior = max(noccur, key=noccur.get)
    valor_cat = noccur.get(cat_maior)

    for valor in noccur.values():
        total += valor

    confianca = valor_cat / total
    return cat_maior,confianca


################################################ TESTING ##################################################################
inp = "Olá. Eu gostava de comprar um bilhete para o cinema na aplicação."
print(inp)
palavras = limpa_texto(inp)
noccur = criar_noccur_dic(palavras)
cat_maior,confianca = calcula_confianca(noccur)
print(cat_maior,confianca)
