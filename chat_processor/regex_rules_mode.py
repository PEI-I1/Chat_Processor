import re

def regexPrice(message):
    message = re.sub(' ', '', message) #remove possíveis espacos
    ret = re.search('^[0-9]+(.[0-9]+)?', message).group()
    return float(ret)


##################################################################
######################## TESTING #################################
##################################################################
def testRegexPrice():
    val = "11.25 €"
    print(regexPrice(val))
