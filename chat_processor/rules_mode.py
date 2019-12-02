import globals #redis_db
from utils import get_content, get_entry
from utils import get_content, get_service
from rules_mode_cinemas import cinema_rules
from rules_mode_fs import fs_rules
from rules_mode_rp import problem_rules


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
        return str('''Escolha uma das seguintes opções, digitando o número correspondente.
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
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
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


