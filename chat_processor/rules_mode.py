import globals #redis_db
from utils import get_content
from regex_rules_mode import regexPrice
import json


def load_redis(idChat, idUser):
    aux = globals.redis_db.get(str(idChat) + str(idUser) + '_rules_mode')

    if aux:
        return int(aux)
    else:
        return 0


def remove_redis(idChat, idUser, chatData):
    chatData["status"] = ''
    globals.redis_db.set(idChat, json.dumps(chatData))
    globals.redis_db.delete(str(idChat) + str(idUser) + '_rules_mode')


def save_redis(idChat, idUser, menu):
    globals.redis_db.set(str(idChat) + str(idUser) + '_rules_mode', menu)


def save_number(idChat, idUser, code, number):
    globals.redis_db.set(str(idChat) + str(idUser) + code, number)


def load_number(idChat, idUser, code):
    aux = globals.redis_db.get(str(idChat) + str(idUser) + code)

    if aux:
        return int(aux)
    else:
        return 0


def remove_number(idChat, idUser, code):
    globals.redis_db.delete(str(idChat) + str(idUser) + code)


def save_float(idChat, idUser, code, number):
    globals.redis_db.set(str(idChat) + str(idUser) + code, number)


def load_float(idChat, idUser, code):
    aux = globals.redis_db.get(str(idChat) + str(idUser) + code)

    if aux:
        return float(aux)
    else:
        return 0.0


def remove_float(idChat, idUser, code):
    globals.redis_db.delete(str(idChat) + str(idUser) + code)


def save_string(idChat, idUser, code, string):
    globals.redis_db.set(str(idChat) + str(idUser) + code, string)


def load_string(idChat, idUser, code):
    aux = globals.redis_db.get(str(idChat) + str(idUser) + code)

    if aux:
        return aux
    else:
        return None


def remove_string(idChat, idUser, code):
    globals.redis_db.delete(str(idChat) + str(idUser) + code)


def final_packages(idChat, idUser):
    aux =  {}
    tipo = load_string(idChat, idUser, '_package_type')
    servico = load_string(idChat, idUser, '_package_service')
    preco = load_string(idChat, idUser, '_package_price')

    if tipo and tipo != 'all':
        aux['type'] = tipo

    if servico and servico != 'all':
        aux['service'] = servico

    if preco and preco != 'all':
        aux['min'] = load_float(idChat, idUser, '_min_value')
        aux['max'] = load_float(idChat, idUser, '_max_value')

    return get_content('/fs_scrapper/packages', [], aux)


def get_response_rules(idChat, idUser, msg, name, chatData):
    menu = load_redis(idChat, idUser)

    if menu == 0:
        save_redis(idChat, idUser, 1)
        return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. cinemas ou sessões\n2. tarifários ou pacotes\n3. compra de telemóveis
4. lojas da NOS\n5. linhas de apoio\n6. resolução de problemas técnicos\n7. exit''')

    elif menu == 1:
        opcao = int(msg)

        if opcao == 1:
            resposta = cinema_rules(idChat, idUser, opcao, msg, chatData)
            return resposta

        elif opcao == 2 or opcao == 3 or opcao == 4 or opcao == 5:
            resposta = fs_rules(idChat, idUser, opcao, msg, chatData)
            return resposta

        elif opcao == 6:
            resposta = problem_rules(idChat, idUser, opcao, msg, chatData)
            return resposta

        elif opcao == 7:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. cinemas ou sessões\n2. tarifários ou pacotes\n3. compra de telemóveis
4. lojas da NOS\n5. linhas de apoio\n6. resolução de problemas técnicos\n7. sair''')

    elif 10 < menu < 20 or 100 < menu < 200:
        resposta = cinema_rules(idChat, idUser, menu, msg, chatData)
        return resposta

    elif 20 < menu < 30 or 200 < menu < 300:
        resposta = fs_rules(idChat, idUser, menu, msg, chatData)
        return resposta

    elif 30 < menu < 40 or 300 < menu < 400:
        resposta = problem_rules(idChat, idUser, menu, msg, chatData)
        return resposta

    else:
        return str("Pedimos desculpa, mas algo correu mal.")


def cinema_rules(idChat, idUser, menu, msg, chatData):
    try:
        opcao = int(msg)
    except ValueError:
        opcao = -1

    if menu == 1:
        save_redis(idChat, idUser, 11)
        return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar cinemas\n2. procurar filmes em sessão\n3. procurar filmes por parametro
4. buscar próximas estreias\n5. buscar informação de um filme\n6. procurar sessões sobre uma duração específica
7. procurar pelas próximas sessões\n8. procurar sessões de um filme\n9. procurar sessões por datas\n10. sair''')

    elif menu == 11:
        if opcao == 1:
            #TODO Search for cinemas or get the closest ones
            remove_redis(idChat, idUser, chatData)
        elif opcao == 2:
            #TODO Search for movies in cinema
            remove_redis(idChat, idUser, chatData)
        elif opcao == 3:
            #TODO Search for movies based on genre, producer, cast, synopsis and age restriction
            remove_redis(idChat, idUser, chatData)
        elif opcao == 4:
            #TODO Search for upcoming movies
            remove_redis(idChat, idUser, chatData)
        elif opcao == 5:
            #TODO Get details of movie
            remove_redis(idChat, idUser, chatData)
        elif opcao == 6:
            #TODO Search for sessions of movies under a certain duration
            remove_redis(idChat, idUser, chatData)
        elif opcao == 7:
            #TODO Search for the next sessions
            remove_redis(idChat, idUser, chatData)
        elif opcao == 8:
            #TODO Search sessions for a given movie
            remove_redis(idChat, idUser, chatData)
        elif opcao == 9:
            #TODO Search for sessions by date
            remove_redis(idChat, idUser, chatData)
        elif opcao == 10:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar cinemas\n2. procurar filmes em sessão\n3. procurar filmes por parametro
4. buscar próximas estreias\n5. buscar informação de um filme\n6. procurar sessões sobre uma duração específica
7. procurar pelas próximas sessões\n8. procurar sessões de um filme\n9. procurar sessões por datas\n10. sair''')


def fs_rules(idChat, idUser, menu, msg, chatData):
    try:
        opcao = int(msg)
    except ValueError:
        opcao = -1

    if menu == 2:
        save_redis(idChat, idUser, 21)
        return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. tarifários WTF\n2. pacotes\n3. sair''')

    elif menu == 3:
        save_redis(idChat, idUser, 22)
        #TODO menu dos telemóveis, ir por passos como fiz para os pacotes (ex: 1º perguntar se quer marca específica, depois perguntar se quer novos lançamentos, etc)
        return None

    elif menu == 4:
        save_redis(idChat, idUser, 23)
        return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. indicar uma zona para procura de lojas\n2. lojas perto da sua localização atual\n3. sair''')

    elif menu == 5:
        save_redis(idChat, idUser, 24)
        return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. linha de apoio de acordo com o assunto\n2. todas as linhas de apoio\n3. sair''')

    elif menu == 21:
        if opcao == 1:
            save_redis(idChat, idUser, 25)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar todo os tarifários WTF\n2. tarifários WTF por nome\n3. sair''')
        elif opcao == 2:
            save_redis(idChat, idUser, 26)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. indicar nome de um pacote\n2. fazer pesquisa sobre pacotes\n3. sair''')
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. tarifários WTF\n2. pacotes\n3. sair''')

    elif menu == 22:
        #TODO
        return None

    elif menu == 23:
        if opcao == 1:
            save_redis(idChat, idUser, 231)
            return str("Indique uma zona ou morada para a qual procura lojas NOS.")
        elif opcao == 2:
            save_redis(idChat, idUser, 232)
            return str("Precisamos do seu consentimento para aceder à sua localização atual. Se consentir, por favor digite 1. Caso contrário, digite qualquer outra tecla.")
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. indicar uma zona para procura de lojas\n2. lojas perto da sua localização atual\n3. sair''')

    elif menu == 24:
        if opcao == 1:
            save_redis(idChat, idUser, 241)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Serviços NOS\n2. Entidades\n3. Equipamentos NOS\n4. Denúncia Fraude/Pirataria\n5. Faturas Contencioso\n6. Informações
7. sair''')
        if opcao == 2:
            requerido = get_content('/fs_scrapper/linhas_apoio', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. linha de apoio de acordo com o assunto\n2. todas as linhas de apoio\n3. sair''')

    elif menu == 25:
        if opcao == 1:
            requerido = get_content('/fs_scrapper/wtf', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            save_redis(idChat, idUser, 251)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. WTF 1GB\n2. WTF 5GB\n3. WTF 10GB\n4. sair''')
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar todo os tarifários WTF\n2. tarifários WTF por nome\n3. sair''')

    elif menu == 26:
        if opcao == 1:
            save_redis(idChat, idUser, 261)
            return str('''Indique o nome do pacote pretendido.''')
        elif opcao == 2:
            save_redis(idChat, idUser, 262)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. pacotes fibra\n2. pacotes satélite\n3. todos os tipos de pacotes\n4. sair''')
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. indicar nome de um pacote\n2. fazer pesquisa sobre pacotes\n3. sair''')

    elif menu == 231:
        aux = {}
        aux['search_term'] = msg
        requerido = get_content('/fs_scrapper/stores', [], aux)
        remove_redis(idChat, idUser, chatData)
        return requerido

    elif menu == 232:
        if opcao == 1:
            #TODO confirmar que basta fazer isto para aceder à localização !!!!!!!!
            aux = {}
            aux['lat'] = float(chatData['locationParam']['lat'])
            aux['lon'] = float(chatData['locationParam']['lon'])
            requerido = get_content('/fs_scrapper/stores', [], aux)
            remove_redis(idChat, idUser, chatData)
            return None
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

    elif menu == 241:
        if opcao == 1:
            save_redis(idChat, idUser, 242)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Pacotes com Televisão\n 2. Telemóvel\n 3. Internet Fixa\n 4. Internet Móvel\n 5. Telefone
6. Ativação de Pacotes Internet\n 7. Apoio Informático\n8. Sair''')
        elif opcao == 2:
            save_redis(idChat, idUser, 243)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Empresas\n 2. Corporate\n 3. Profissionais e Empresas\n 4. Particulares\n5. Sair''')
        elif opcao == 3:
            save_redis(idChat, idUser, 244)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Reparação de Equipamentos\n 2. Devolução de Equipamentos\n3. Sair''')
        elif opcao == 4:
            aux = {}
            aux['subject'] = "Denúncia de fraude / pirataria"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 5:
            aux = {}
            aux['subject'] = "Contencioso"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 6:
            save_redis(idChat, idUser, 245)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Info Portabilidade\n 2. Video Intérprete\n3. Sair''')
        elif opcao == 7:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Serviços NOS\n2. Entidades\n3. Equipamentos NOS\n4. Denúncia Fraude/Pirataria\n5. Faturas Contencioso\n6. Informações
7. sair\n''')

    elif menu == 242:
        if opcao == 1:
            aux = {}
            aux['subject'] = "Pacotes com televisão"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            aux = {}
            aux['subject'] = "Telemóvel"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            aux = {}
            aux['subject'] = "Internet fixa"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 4:
            aux = {}
            aux['subject'] = "Internet móvel"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 5:
            aux = {}
            aux['subject'] = "Telefone"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 6:
            aux = {}
            aux['subject'] = "Ativação pacotes internet"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 7:
            aux = {}
            aux['subject'] = "Apoio informático"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 8:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Pacotes com Televisão\n 2. Telemóvel\n 3. Internet Fixa\n 4. Internet Móvel\n 5. Telefone
6. Ativação de Pacotes Internet\n 7. Apoio Informático\n8. Sair''')

    elif menu == 243:
        if opcao == 1:
            aux = {}
            aux['subject'] = "Empresas"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            aux = {}
            aux['subject'] = "Corporate"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            aux = {}
            aux['subject'] =  "Profissionais e empresas"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 4:
            aux = {}
            aux['subject'] = "Particulares"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 5:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Empresas\n 2. Corporate\n 3. Profissionais e Empresas\n 4. Particulares\n5. Sair''')

    elif menu == 244:
        if opcao == 1:
            aux = {}
            aux['subject'] = "Reparação de equipamentos"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            aux = {}
            aux['subject'] = "Devolução de equipamentos NOS"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Reparação de Equipamentos\n 2. Devolução de Equipamentos\n3. Sair''')

    elif menu == 245:
        if opcao == 1:
            aux = {}
            aux['subject'] = "Video intérprete"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            aux = {}
            aux['subject'] = "InfoPortabilidade"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Info Portabilidade\n 2. Video Intérprete\n3. Sair''')

    elif menu == 251:
        if opcao == 1:
            aux = {}
            aux['nome'] = 'WTF 1GB'
            requerido = get_content('/fs_scrapper/wtf_name', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            aux = {}
            aux['nome'] = 'WTF 5GB'
            requerido = get_content('/fs_scrapper/wtf_name', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            aux = {}
            aux['nome'] = 'WTF 10GB'
            requerido = get_content('/fs_scrapper/wtf_name', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. WTF 1GB\n2. WTF 5GB\n3. WTF 10GB\n4. sair''')

    elif menu == 261:
        aux = {}
        aux['name'] = msg
        requerido = get_content('/fs_scrapper/packages', [], aux)
        remove_redis(idChat, idUser, chatData)
        return requerido

    elif menu == 262:
        if opcao == 1:
            save_string(idChat, idUser, '_package_type', 'fibra')
            save_redis(idChat, idUser, 263)
            return str('''Escolha um dos seguintes serviços, digitando o número correspondente.
1. TV\n2. NET\n3. TV+NET\n4. TV+VOZ\n5. TV+NET+VOZ\n6. sair''')
        elif opcao == 2:
            save_string(idChat, idUser, '_package_type', 'satelite')
            save_redis(idChat, idUser, 263)
            return str('''Escolha um dos seguintes serviços, digitando o número correspondente.
1. TV\n2. NET\n3. TV+NET\n4. TV+VOZ\n5. TV+NET+VOZ\n6. sair''')
        elif opcao == 3:
            save_string(idChat, idUser, '_package_type', 'all')
            save_redis(idChat, idUser, 263)
            return str('''Escolha um dos seguintes serviços, digitando o número correspondente.
1. TV\n2. NET\n3. TV+NET\n4. TV+VOZ\n5. TV+NET+VOZ\n6. sair''')
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. pacotes fibra\n2. pacotes satélite\n3. todos os tipos de pacotes\n4. sair''')

    elif menu == 263:
        if opcao == 1:
            save_string(idChat, idUser, '_package_service', 'TV')
            save_redis(idChat, idUser, 264)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. definir intervalo de preços\n2. qualquer preço\n3. sair''')
        elif opcao == 2:
            save_string(idChat, idUser, '_package_service', 'NET')
            save_redis(idChat, idUser, 264)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. definir intervalo de preços\n2. qualquer preço\n3. sair''')
        elif opcao == 3:
            save_string(idChat, idUser, '_package_service', 'TV+NET')
            save_redis(idChat, idUser, 264)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. definir intervalo de preços\n2. qualquer preço\n3. sair''')
        elif opcao == 4:
            save_string(idChat, idUser, '_package_service', 'TV+VOZ')
            save_redis(idChat, idUser, 264)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. definir intervalo de preços\n2. qualquer preço\n3. sair''')
        elif opcao == 5:
            save_string(idChat, idUser, '_package_service', 'TV+NET+VOZ')
            save_redis(idChat, idUser, 264)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. definir intervalo de preços\n2. qualquer preço\n3. sair''')
        elif opcao == 6:
            save_string(idChat, idUser, '_package_service', 'all')
            save_redis(idChat, idUser, 264)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. definir intervalo de preços\n2. qualquer preço\n3. sair''')
        elif opcao == 7:
            remove_string(idChat, idUser, '_package_type')
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha um dos seguintes serviços, digitando o número correspondente.
1. TV\n2. NET\n3. TV+NET\n4. TV+VOZ\n5. TV+NET+VOZ\n6. indiferenciado\n7. sair''')

    elif menu == 264:
        if opcao == 1:
            save_string(idChat, idUser, '_package_price', 'defined')
            save_redis(idChat, idUser, 265)
            return str("Indique o valor mínimo que procura.")
        elif opcao == 2:
            save_string(idChat, idUser, '_package_price', 'all')
            required = final_packages(idChat, idUser)
            remove_string(idChat, idUser, '_package_type')
            remove_string(idChat, idUser, '_package_service')
            remove_string(idChat, idUser, '_package_price')
            remove_redis(idChat, idUser, chatData)
            return required
        elif opcao == 3:
            remove_string(idChat, idUser, '_package_type')
            remove_string(idChat, idUser, '_package_service')
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. definir intervalo de preços\n2. qualquer preço\n3. sair''')

    elif menu == 265:
        try:
            valorMin = regexPrice(msg)
            save_float(idChat, idUser, '_min_value', valorMin)
            save_redis(idChat, idUser, 266)
            return str("Indique o valor máximo que procura.\n")
        except:
            return str("Por favor, volte a tentar inserindo o valor com dígitos e .")

    elif menu == 266:
        try:
            valorMax = regexPrice(msg)
            save_float(idChat, idUser, '_max_value', valorMax)
            save_redis(idChat, idUser, 267)
            required = final_packages(idChat, idUser)
            remove_string(idChat, idUser, '_package_type')
            remove_string(idChat, idUser, '_package_service')
            remove_string(idChat, idUser, '_package_price')
            remove_float(idChat, idUser, '_min_value')
            remove_float(idChat, idUser, '_max_value')
            remove_redis(idChat, idUser, chatData)
            return required
        except:
            return str("Por favor, volte a tentar inserindo o valor com dígitos e .")


def problem_rules(idChat, idUser, menu, msg, chatData):
    #TODO
    return ""
