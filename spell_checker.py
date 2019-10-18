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

def spell_check(string):
    page = get_page(string)
    return get_spell(page, string)
