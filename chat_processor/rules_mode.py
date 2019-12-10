import globals #redis_db
from utils import get_content


def load_redis(idChat, idUser):
    aux = globals.redis_db.get(idChat + idUser + '_rules_mode')

    if aux:
        return int(aux)
    else:
        return 0


def save_redis(idChat, idUser, menu):
    globals.redis_db.set(idChat + idUser + '_rules_mode', menu)


def remove_redis(idChat, idUser, chatData):
    chatData["status"] = ''
    globals.redis_db.set(idChat, chatData)
    globals.redis_db.delete(idChat + idUser + '_rules_mode')


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
            return str("Saiu do modo de regras")
    
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
        return str('''Escolha uma das seguintes opções, digitando o número correspondente.\n
1. procurar cinemas\n
2. procurar filmes em sessão\n
3. procurar filmes por parametro\n
4. buscar próximas estreias\n
5. buscar informação de um filme\n
6. procurar sessões sobre uma duração específica\n
7. procurar pelas próximas sessões\n
8. procurar sessões de um filme\n
9. procurar sessões por datas\n
10. sairn\n''')

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
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")


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
        return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar modelo de telemóvel\n2. procurar telemóvel por marca\n3. apresentar top de telemóveis mais procurados
4. apresentar telemóveis em promoção\n5. apresentar telemóveis mais recentes
6. apresentar telemóveis com ofertas\n7. apresentar telemóveis com opção de pagamento a prestações
8. apresentar telemóveis com opção de pagamento com pontos
9. procurar telemóveis dentro de uma gama de valores\n10. sair''')

    elif menu == 4:
        save_redis(idChat, idUser, 23)
        return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. lojas por cidade\n2. informações relativas a uma loja\n3. sair''')

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
1. apresentar pacotes de satélite\n2. apresentar pacotes com fibra
3. apresentar pacotes por serviço (TV+NET+VOZ, TV+NET, ...)\n4. apresentar pacotes por preço\n5. sair''')
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. tarifários WTF\n2. pacotes\n3. sair''')

    elif menu == 22:
        if opcao == 1:
            save_redis(idChat, idUser, 27)
            return str('''Escreva o modelo que procura\n''')
        elif opcao == 2:
            save_redis(idChat, idUser, 28)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar telemóveis por marca\n 2. procurar telemóveis por marca numa gama de valores
3. procurar telemóveis por marca com promoção\n4. procurar telemóveis mais recentes de uma marca\n5. sair''')
        elif opcao == 3:
            requerido = get_content('/fs_scrapper/top_phones', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 4:
            save_redis(idChat, idUser, 206)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar telemóveis em promoção\n2. procurar telemóveis por marca com promoção
3. procurar telemóveis em promoção numa gama de valores\n4. sair''')
        elif opcao == 5:
            save_redis(idChat, idUser, 207)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar telemóveis mais recentes\n 2. procurar telemóveis mais recentes de uma marca\n3. sair''')
        elif opcao == 6:
            requerido = get_content('/fs_scrapper/ofer_phones', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 7:
            requerido = get_content('/fs_scrapper/prest_phones', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 8:
            requerido = get_content('/fs_scrapper/points_phones', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 9:
            save_redis(idChat, idUser, 208)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar telemóveis numa gama de valores\n 2. procurar telemóveis por marca numa gama de valores
3. procurar telemóveis em promoção numa gama de valores\n4. sair''')
        elif opcao == 10:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar modelo de telemóvel\n2. procurar telemóvel por marca\n3. apresentar top de telemóveis mais procurados
4. apresentar telemóveis em promoção\n5. apresentar telemóveis mais recentes
6. apresentar telemóveis com ofertas\n7. apresentar telemóveis com opção de pagamento a prestações
8. apresentar telemóveis com opção de pagamento com pontos
9. procurar telemóveis dentro de uma gama de valores\n10. sair''')

    elif menu == 23:
        if opcao == 1:
            save_redis(idChat, idUser, 29)
            return str('''Indique o nome do local onde deseja procurar lojas NOS.''')
        elif opcao == 2:
            save_redis(idChat, idUser, 201)
            return str('''Indique a morada da loja NOS desejada.''')
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. lojas por cidade\n2. informações relativas a uma loja\n3. sair''')

    elif menu == 24:
        if opcao == 1:
            save_redis(idChat, idUser, 202)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente. 
1. Serviços NOS\n2. Entidades\n3. Equipamentos NOS\n4. Denúncia Fraude/Pirataria\n5. Faturas Contencioso\n6. Informações
7. sair''')
        if opcao == 2:
            requerido = get_content('/fs_scrapper/linhas_apoio', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. linha de apoio de acordo com o assunto\n2. todas as linhas de apoio\n3. sair''')

    elif menu == 25:
        if opcao == 1:
            requerido = get_content('/fs_scrapper/all_wtf', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            save_redis(idChat, idUser, 203)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. WTF 1GB\n2. WTF 5GB\n3. WTF 10GB\n4. sair''')
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar todo os tarifários WTF\n2. tarifários WTF por nome\n3. sair''')

    elif menu == 26:
        if opcao == 1:
            save_redis(idChat, idUser, 209)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar pacotes com satélite\n2. procurar pacotes com satélite numa gama de valores
3. procurar pacotes com satélite por serviço\n4. sair''')
        elif opcao == 2:
            save_redis(idChat, idUser, 210)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar pacotes com fibra\n2. procurar pacotes com fibra numa gama de valores
3. procurar pacotes com fibra por serviço\n4. sair''')
        elif opcao == 3:
            save_redis(idChat, idUser, 211)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar pacotes por serviço\n2. procurar pacotes por serviço numa gama de valores
3. procurar pacotes com satélite por serviço\n4. procurar pacotes com fibra por serviço\n5. sair''')
        elif opcao == 4:
            save_redis(idChat, idUser, 212)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar pacotes numa gama de valores\n2. procurar pacotes por serviço numa gama de valores
3. procurar pacotes com satélite numa gama de valores\n4. procurar pacotes com fibra numa gama de valores\n5. sair''')
        elif opcao == 5:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar pacotes de satélite\n2. apresentar pacotes com fibra
3. apresentar pacotes por serviço (TV+NET+VOZ, TV+NET, ...)\n4. apresentar pacotes por preço\n5. sair''')

    elif menu == 28:
        if opcao == 1:
            #TODO procurar telemóvel por marca -- TEM QUE SE ENVIAR MENU DE PERGUNTA AO USER, EX OPÇOES DO MENU 23
            return None
        elif opcao == 2:
            #TODO procurar telemóvel por marca numa gama de valores -- TEM QUE SE ENVIAR MENU DE PERGUNTA AO USER, EX OPÇOES DO MENU 23
            return None
        elif opcao == 3:
            #TODO procurar telms por marca que estejam em promoção -- TEM QUE SE ENVIAR MENU DE PERGUNTA AO USER, EX OPÇOES DO MENU 23
            return None
        elif opcao == 4:
            #TODO procurar telms por marca mais recentes -- TEM QUE SE ENVIAR MENU DE PERGUNTA AO USER, EX OPÇOES DO MENU 23
            return None
        elif opcao == 5:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar telemóvel por marca\n 2. Procurar telemóvel por marca numa gama de valores
3. procurar por telemóvel por marca com promoção\nprocurar telemóveis mais recentes de uma marca\n5. sair''')

    elif menu == 29:
        aux = []
        aux.append(msg)
        requerido = get_content('/fs_scrapper/stores_zone', aux, {})
        remove_redis(idChat, idUser, chatData)
        return requerido

    elif menu == 201:
        aux = []
        aux.append(msg)
        requerido = get_content('/fs_scrapper/store_address', aux, {})
        remove_redis(idChat, idUser, chatData)
        return requerido

    elif menu == 202:
        if opcao == 1:
            save_redis(idChat,idUser,241)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Pacotes com Televisão\n 2. Telemóvel\n 3. Internet Fixa\n 4. Internet Móvel\n 5. Telefone 
6. Ativação de Pacotes Internet\n 7. Apoio Informático\n8. Sair''')
        elif opcao == 2:
            save_redis(idChat, idUser, 242)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Empresas\n 2. Corporate\n 3. Profissionais e Empresas\n 4. Particulares\n5. Sair''')
        elif opcao == 3:
            save_redis(idChat, idUser, 243)
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
            save_redis(idChat, idUser, 244)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Info Portabilidade\n 2. Video Intérprete\n3. Sair''')
        elif opcao == 7:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente. 
1. Serviços NOS\n2. Entidades\n3. Equipamentos NOS\n4. Denúncia Fraude/Pirataria\n5. Faturas Contencioso\n6. Informações
7. sair\n''')

    elif menu == 203:
        if opcao == 1:
            aux = []
            aux.append('WTF 1GB')
            requerido = get_content('/fs_scrapper/wtf_name', aux, {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            aux = []
            aux.append('WTF 5GB')
            requerido = get_content('/fs_scrapper/wtf_name', aux, {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            aux = []
            aux.append('WTF 10GB')
            requerido = get_content('/fs_scrapper/wtf_name', aux, {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. WTF 1GB\n2. WTF 5GB\n3. WTF 10GB\n4. sair''')

    elif menu == 206:
        if opcao == 1:
            #TODO tlms em promoção
            return None
        elif opcao == 2:
            #TODO tlms em promoção por marca
            return None
        elif opcao == 3:
            #TODO tlms em promoção em gama de valores
            return None
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar telemóveis em promoção\n 2. procurar telemóveis por marca com promoção
3. procurar telemóveis em promoção numa gama de valores\n4. sair''')

    elif menu == 207:
        if opcao == 1:
            #TODO tlms mais recentes
            return None
        elif opcao == 2:
            #TODO tlms mais recentes por marca
            return None
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar telemóveis mais recentes\n 2. procurar telemóveis mais recentes de uma marca\n3. sair''')

    elif menu == 208:
        if opcao == 1:
            #TODO tlms numa gama de valores
            return None
        elif opcao == 2:
            #TODO tlms numa gama de valores por marca
            return None
        elif opcao == 3:
            #TODO tlms numa gama de valores em promoção
            return None
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar telemóveis numa gama de valores\n 2. procurar telemóveis por marca numa gama de valores
3. procurar telemóveis em promoção numa gama de valores\n4. sair''')

    elif menu == 209:
        if opcao == 1:
            #TODO pacotes satelite
            return None
        elif opcao == 2:
            #TODO pacotes satelite por preço
            return None
        elif opcao == 3:
            #TODO pacotes satelite por serviço
            return None
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar pacotes com satélite\n2. procurar pacotes com satélite numa gama de valores
3. procurar pacotes com satélite por serviço\n4. sair''')

    elif menu == 210:
        if opcao == 1:
            #TODO pacotes fibra
            return None
        elif opcao == 2:
            #TODO pacotes fibra por preço
            return None
        elif opcao == 3:
            #TODO pacotes fibra por serviço
            return None
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar pacotes com fibra\n2. procurar pacotes com fibra numa gama de valores
3. procurar pacotes com fibra por serviço\n4. sair''')

    elif menu == 211:
        if opcao == 1:
            #TODO pacotes por serviço
            return None
        elif opcao == 2:
            #TODO pacotes por serviço por preço
            return None
        elif opcao == 3:
            #TODO pacotes satelite por serviço
            return None
        elif opcao == 4:
            #TODO pacotes fibra por serviço
            return None
        elif opcao == 5:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar pacotes por serviço\n2. procurar pacotes por serviço numa gama de valores
3. procurar pacotes com satélite por serviço\n4. procurar pacotes com fibra por serviço\n5. sair''')

    elif menu == 212:
        if opcao == 1:
            #TODO pacotes por preço
            return None
        elif opcao == 2:
            #TODO pacotes por serviço por preço
            return None
        elif opcao == 3:
            #TODO pacotes satelite por preço
            return None
        elif opcao == 4:
            #TODO pacotes fibra por preço
            return None
        elif opcao == 5:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. procurar pacotes numa gama de valores\n2. procurar pacotes por serviço numa gama de valores
3. procurar pacotes com satélite numa gama de valores\n4. procurar pacotes com fibra numa gama de valores\n5. sair''')

    elif menu == 220:           #TODO temos que alterar este menu !!!!
            print('''Insira o limite Inferior''')
            limInf = input()
            print('''Insira o limite Superior''')
            limSup = input()
            return None

    elif menu == 241:
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
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Pacotes com Televisão\n 2. Telemóvel\n 3. Internet Fixa\n 4. Internet Móvel\n 5. Telefone 
6. Ativação de Pacotes Internet\n 7. Apoio Informático\n8. Sair''')

    elif menu == 242:
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
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Empresas\n 2. Corporate\n 3. Profissionais e Empresas\n 4. Particulares\n5. Sair''')

    elif menu == 243:
        if opcao == 1:
            aux = {}
            aux['subject'] =  "Reparação de equipamentos"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            aux = {}
            aux['subject'] =  "Devolução de equipamentos NOS"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Reparação de Equipamentos\n 2. Devolução de Equipamentos\n3. Sair''')

    elif menu == 244:
        if opcao == 1:
            aux = {}
            aux['subject'] =  "Video intérprete"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 2:
            aux = {}
            aux['subject'] =  "InfoPortabilidade"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. Info Portabilidade\n 2. Video Intérprete\n3. Sair''')

    else:
        return str("Pedimos desculpa, mas algo correu mal.")


def problem_rules(idChat, idUser, menu, msg, chatData):
    #TODO
    return ""

