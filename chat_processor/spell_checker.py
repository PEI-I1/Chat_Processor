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

# =====  symspellpy ======
import os
from symspellpy.symspellpy import SymSpell
sym_spell = None

def init():
    global sym_spell
    max_edit_distance_dictionary = 2
    prefix_length = 7

    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    #sym_spell.load_dictionary(os.path.dirname(os.path.abspath(__file__)) + "/frequency_words_models/pt_frequency_50k.txt", term_index=0, count_index=1)
    sym_spell.load_dictionary(os.path.dirname(os.path.abspath(__file__)) + "/frequency_words_models/fw_pt.txt", term_index=0, count_index=1)
    sym_spell.load_bigram_dictionary(os.path.dirname(os.path.abspath(__file__)) + "/frequency_words_models/fw_bi_pt.txt", term_index=0, count_index=2)

"""
Devolve a string corrigida.

Argumentos:
string -- texto a corrigir
"""
def spell_check_ss(string):
    global sym_spell
    max_edit_distance_lookup = 2

    suggestions = sym_spell.lookup_compound(string, max_edit_distance_lookup)
    return suggestions[0].term
