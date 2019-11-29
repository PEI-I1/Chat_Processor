import globals #redis_db
from utils import get_content, get_service


def load_redis(idChat, idUser):
    #TODO carregar int do redis, caso não exista returnar 0
    return 0


def save_redis(idChat, idUser, menu):
    #TODO guardar int do menu no redis
    return None


def remove_redis(idChat, idUser):
    #TODO utilizador quer sair do modo regras, remover entrada do redis
    return None


def get_response_rules(idChat, idUser, msg, name):
    menu = load_redis(idChat, idUser)

    if menu == 0:
        save_redis(idChat, idUser, 1)
        return str('''Escolha uma das seguintes opções, indicando o número correspondente.
1. cinemas ou sessões\n2. tarifários ou pacotes\n3. compra de telemóveis
4. lojas da NOS\n5. linhas de apoio\n6. resolução de problemas técnicos\n7. exit''')

    elif menu == 1:
        opcao = int(msg)

        if opcao == 1:
            resposta = cinema_rules(idChat, idUser, opcao, msg)
            return resposta

        elif opcao == 2 or opcao == 3 or opcao == 4 or opcao == 5:
            resposta = fs_rules(idChat, idUser, opcao, msg)
            return resposta

        elif opcao == 6:
            resposta = problem_rules(idChat, idUser, opcao, msg)
            return resposta

        elif opcao == 7:
            remove_redis(idChat, idUser)
            return None         # o que fazer quando se sai do modo regas?
    
        else:
            return str('''Escolha uma das seguintes opções, indicando o número correspondente.
1. cinemas ou sessões\n2. tarifários ou pacotes\n3. compra de telemóveis
4. lojas da NOS\n5. linhas de apoio\n6. resolução de problemas técnicos\n7. sair''')

    elif 10 < menu < 20 or 100 < menu < 200:
        resposta = cinema_rules(idChat, idUser, menu, msg)
        return resposta

    elif 20 < menu < 30 or 200 < menu < 300:
        resposta = fs_rules(idChat, idUser, menu, msg)
        return resposta

    elif 30 < menu < 40 or 300 < menu < 400:
        resposta = problem_rules(idChat, idUser, menu, msg)
        return resposta

    else:
        return str("Pedimos desculpa, mas algo correu mal.")


def cinema_rules(idChat, idUser, menu, msg):
    #TODO
    return ""


def fs_rules(idChat, idUser, menu, msg):
    if menu == 2:
        save_redis(idChat, idUser, 21)
        return str('''Escolha uma das seguintes opções, indicando o número correspondente.
1. tarifários WTF\n2. pacotes\n3. sair''')

    elif menu == 3:
        save_redis(idChat, idUser, 22)
        return str('''Escolha uma das seguintes opções, indicando o número correspondente.
1. procurar modelo de telemóvel\n2. procurar telemóvel por marca\n3. apresentar top de telemóveis mais procurados
4. apresentar telemóveis em promoção\n5. apresentar telemóveis mais recentes
6. apresentar telemóveis com ofertas\n7. apresentar telemóveis com opção de pagamento a prestações
8. apresentar telemóveis com opção de pagamento com pontos
9. procurar telemóveis dentro de uma gama de valores\n10. sair''')

    elif menu == 4:
        save_redis(idChat, idUser, 23)
        return str('''Escolha uma das seguintes opções, indicando o número correspondente.
1. lojas por cidade\n2. informações relativas a uma loja\n3. sair''')

    elif menu == 5:
        save_redis(idChat, idUser, 24)
        return str('''Escolha uma das seguintes opções, indicando o número correspondente.
1. linha de apoio de acordo com o assunto\n2. todas as linhas de apoio\n3. sair''')

    elif menu == 21:
        opcao = int(msg)

        if opcao == 1:
            save_redis(idChat, idUser, 25)
            return str('''Escolha uma das seguintes opções, indicando o número correspondente.
1. apresentar todo os tarifários WTF\n2. tarifários WTF por nome\n3. sair''')

        elif opcao == 2:
            #TODO   falta menu dos pacotes

        elif opcao == 3:
            remove_redis(idChat, idUser)
            return None

        else:
            return str('''Escolha uma das seguintes opções, indicando o número correspondente.
1. tarifários WTF\n2. pacotes\n3. sair''')

    #TODO continuar menus a partir do 21

    else:
        return str("Pedimos desculpa, mas algo correu mal.")


def problem_rules(idChat, idUser, menu, msg):
    #TODO
    return ""

