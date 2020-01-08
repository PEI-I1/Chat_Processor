import re

def regexPrice(message):
    message = re.sub(r'\s+|€|euros?', '', message) #remove possíveis espacos
    message = re.sub(r',', '.', message)
    ret = re.search(r'^[0-9]+(\.[0-9]+)?$', message).group()
    return float(ret)
