from rules_mode import load_redis, remove_redis, save_redis

def fs_rules(idChat, idUser, menu, msg):
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
            remove_redis(idChat, idUser)
            return None

        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. tarifários WTF\n2. pacotes\n3. sair''')

    elif menu == 23:
        if opcao == 1:
            save_redis(idChat, idUser, 29)
            return str('''Indique o nome do local onde deseja procurar lojas NOS.''')

        elif opcao == 2:
            save_redis(idChat, idUser, 201)
            return str('''Indique a morada da loja NOS desejada.''')

        elif opcao == 3:
            remove_redis(idChat, idUser)
            return None

        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. lojas por cidade\n2. informações relativas a uma loja\n3. sair''')

    elif menu == 25:
        if opcao == 1:
            remove_redis(idChat, idUser)
            #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver todos os tarifários wtf

        elif opcao == 2:
            save_redis(idChat, idUser, 203)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. WTF 1GB\n2. WTF 5GB\n3. WTF 10GB\n4. sair''')

        elif opcao == 3:
            remove_redis(idChat, idUser)
            return None

        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. apresentar todo os tarifários WTF\n2. tarifários WTF por nome\n3. sair''')

    elif menu == 29:
        remove_redis(idChat, idUser)
        #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver todas as lojas nos na zona da msg

    elif menu == 201:
        remove_redis(idChat, idUser)
        #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver a loja nos correspondente à morada da msg

    elif menu == 203:
        if opcao == 1:
            nome = 'WTF 1GB'
            remove_redis(idChat, idUser)
            #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver tarifário wtf do nome

        elif opcao == 2:
            nome = 'WTF 5GB'
            remove_redis(idChat, idUser)
            #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver tarifário wtf do nome

        elif opcao == 3:
            nome = 'WTF 10GB'
            remove_redis(idChat, idUser)
            #TODO perguntar ao zé como fazer o pedido aos scrappers -- devolver tarifário wtf do nome

        else:
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
1. WTF 1GB\n2. WTF 5GB\n3. WTF 10GB\n4. sair''')

    #TODO continuar menus

    else:
        return str("Pedimos desculpa, mas algo correu mal.")