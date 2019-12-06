import globals #redis_db
from utils import get_content, get_entry
from utils import get_content, get_service


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
    opcao = int(msg)

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
            #todo Search for cinemas or get the closest ones
            remove_redis(idChat, idUser, chatData)
        elif opcao == 2:
            #todo Search for movies in cinema
            remove_redis(idChat, idUser, chatData)
        elif opcao == 3:
            #todo Search for movies based on genre, producer, cast, synopsis and age restriction
            remove_redis(idChat, idUser, chatData)
        elif opcao == 4:
            #todo Search for upcoming movies
            remove_redis(idChat, idUser, chatData)
        elif opcao == 5:
            #todo Get details of movie
            remove_redis(idChat, idUser, chatData)
        elif opcao == 6:
            # todo Search for sessions of movies under a certain duration
            remove_redis(idChat, idUser, chatData)
        elif opcao == 7:
            #todo Search for the next sessions
            remove_redis(idChat, idUser, chatData)
        elif opcao == 8:
            #todo Search sessions for a given movie
            remove_redis(idChat, idUser, chatData)
        elif opcao == 9:
            #todo Search for sessions by date
            remove_redis(idChat, idUser, chatData)
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")


def fs_rules(idChat, idUser, menu, msg, chatData):
    opcao = int(msg)

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
            1. procurar telemóvel por marca\n 2. Procurar telemóvel por marca numa gama de valores\n
3. procurar por telemóvel por marca com promoção\n4. Sair''')
        elif opcao == 3:
            #todo ir buscar top phones
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 4:
            # todo ir buscar phnes em promoção
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 5:
            # todo ir buscar phones mais recentes
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 6:
            # todo ir buscar phones com oferta
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 7:
            # todo ir buscar possibilidades de prestações
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 8:
            # todo ir buscar phones por pontos
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 9:
            # todo ir buscar com limites menu 220
            save_redis(idChat, idUser, 220)
            return None
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")

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
            1. Serviços NOS\n 2. Entidades\n 3. Equipamentos NOS\n 4. Denúncia\n 5. Faturas\n 6. Informações\n
7. sair\n''')

        if opcao == 2:
            # TODO fazer pedido aos scrappers -- devolver todas as linhas de apoio
            return None
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
    elif menu == 25:
        if opcao == 1:
            remove_redis(idChat, idUser, chatData)
            #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver todos os tarifários wtf

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

    elif menu == 28:
        if opcao == 1:
            #todo procurar telemóvel por marca
            return None
        elif opcao == 2:
            #todo procurar telemóvel por marca numa gama de valores
            return None
        elif opcao == 3:
            #todo procurar telms por marca que estejam em promoção
            return None
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")

    elif menu == 29:
        remove_redis(idChat, idUser, chatData)
        #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver todas as lojas nos na zona da msg

    elif menu == 201:
        remove_redis(idChat, idUser, chatData)
        #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver a loja nos correspondente à morada da msg

    elif menu == 202:
        if opcao == 1:
            save_redis(idChat,idUser,241)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
            1. Pacotes com Televisão\n 2. Telemóvel\n 3. Internet Fixa\n 4. Internet Móvel\n 5. Telefone\n 
6. Ativação de Pacotes Internet\n 7. Apoio Informático\n8. Sair''')
        elif opcao == 2:
            save_redis(idChat, idUser, 242)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. Empresas\n 2. Corporate\n 3. Profissionais e Empresas\n 4. Particulares\n5. Sair''')
        elif opcao == 3:
            save_redis(idChat, idUser, 243)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. Reparação de Equipamentos\n 2. Devolução de Equipamentos\n3. Sair\n 4.Sair''')
        elif opcao == 4:
            save_redis(idChat, idUser, 244)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. Denúncia de Fraude/Pirataria\n2. Sair''')
        elif opcao == 5:
            save_redis(idChat, idUser, 245)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. «Contencioso\n2.Sair''')
        elif opcao == 6:
            save_redis(idChat, idUser, 246)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. Info Portabilidade\n 2. Video Intérprete\n3. Sair''')
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")

    elif menu == 203:
        if opcao == 1:
            nome = 'WTF 1GB'
            remove_redis(idChat, idUser, chatData)
            #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver tarifário wtf do nome

        elif opcao == 2:
            nome = 'WTF 5GB'
            remove_redis(idChat, idUser, chatData)
            #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver tarifário wtf do nome

        elif opcao == 3:
            nome = 'WTF 10GB'
            remove_redis(idChat, idUser, chatData)
            #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver tarifário wtf do nome

        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. WTF 1GB\n2. WTF 5GB\n3. WTF 10GB\n4. sair''')

    elif menu == 220:
            print('''Insira o limite Inferior''')
            limInf = input()
            print('''Insira o limite Superior''')
            limSup = input()
            #todo ir buscar
            return None

    elif menu == 241:
        if opcao == 1:
            #todo scrappers ir buscar pacotes nos com televisão
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 2:
            #todo scrappers ir buscar telemóveis
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 3:
            #todo scrappers ir buscar internet fixa
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 4:
            #todo scrappers ir buscar internet movel
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 5:
            #todo scrappers ir buscar telefone
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 6:
            #todo scrappers ir buscar ativação de pacotes internet
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 7:
            # todo scrappers ir buscar apoio infotmático
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            # sair
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")

    elif menu == 242:
        if opcao == 1:
            #todo scrappers ir buscar empresas
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 2:
            # todo scrappers ir buscar corporate
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 3:
            # todo scrappers ir buscar profissionais e empresas
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 4:
            # todo scrappers ir buscar Particulares
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            # sair
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
    elif menu == 243:
        if opcao == 1:
            #todo ir buscar reparacao equipamentos
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 2:
            # todo ir buscar reparacao equipamentos
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
    elif menu == 244:
        if opcao == 1:
            # todo ir buscar denuncia de pirataria
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
    elif menu == 245:
        if opcao == 1:
            # todo ir buscar faturas contencioso
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
    elif menu == 246:
        if opcao == 1:
            # todo ir buscar informações video interprete
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        elif opcao == 2:
            # todo ir buscar info portabilidade
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras")

    # TODO continuar menus
    else:
        return str("Pedimos desculpa, mas algo correu mal.")


def problem_rules(idChat, idUser, menu, msg, chatData):
    #TODO
    return ""
