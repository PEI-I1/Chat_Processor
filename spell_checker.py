# ===== from google search =====
from bs4 import BeautifulSoup
import requests
from requests.utils import quote

def get_content(tag):
    try:
        elems = tag.contents
        ret = ''

        for e in elems:
            ret += get_content(e)

        return ret
    except:
        return tag

def get_page(string):
    url = "https://www.google.pt/search?q=" + quote(string)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
    }
    return requests.get(url, headers=headers)

def get_spell(page, string):
    soup = BeautifulSoup(page.text, 'html5lib')
    a = soup.find(id='fprsl')

    if a == None:
        return string
    else:
        return str(get_content(a))

"""
Usa o spell check do google search para realizar
o spell check da string recebida.

Devolve a string corrigida.

Argumentos:
string -- texto a corrigir
"""
def spell_check_google(string):
    page = get_page(string)
    return get_spell(page, string)

# =====  pyspellchecker ======
from spellchecker import SpellChecker

"""
Corrige (spell check) uma lista de palavras.
Devolve uma lista de palavras já corrigidas.

Argumentos:
word_list -- lista de palavras a corrigir
"""
def spell_check_psc(words_list):
    spell = SpellChecker(language='pt')
    ret = []

    for word in words_list:
        misspelled = spell.unknown([word])
        if len(misspelled) == 0:
            ret.append(word)
        else:
            ret.append(spell.correction(word))

    return ret
