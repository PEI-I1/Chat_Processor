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

    elif menu == 24:
        if opcao == 1:
            save_redis(idChat, idUser, 202)
            return str('''Escolha uma das seguintes opções, digitando o número correspondente. 
            1. Serviços NOS\n 2. Entidades\n 3. Equipamentos NOS\n 
            4. Denúncia\n 5. Faturas\n 6. Informações\n 7. sair\n''')

        if opcao == 2:
            # TODO fazer pedido aos scrappers -- devolver todas as linhas de apoio
            return None
        else:
            remove_redis(idChat,idUser)
            return None
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

    elif menu == 202:
        if opcao == 1:
            save_redis(idChat,idUser,241) # todo escolher menu
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
            1. Pacotes com Televisão\n 2. Telemóvel\n 3. Internet Fixa\n 4. Internet Móvel\n 5. Telefone\n 6. Ativação de Pacotes Internet\n 7. Apoio Informático''')
        elif opcao == 2:
            save_redis(idChat, idUser, 242)  # todo escolher menu
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. Empresas\n 2. Corporate\n 3. Profissionais e Empresas\n 4. Particulares\n''')
        elif opcao == 3:
            save_redis(idChat, idUser, 243)  # todo escolher menu
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. Reparação de Equipamentos\n 2. Devolução de Equipamentos\n''')
        elif opcao == 4:
            save_redis(idChat, idUser, 244)  # todo escolher menu
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. Denúncia de Fraude/Pirataria\n''') # todo repensar
        elif opcao == 5:
            save_redis(idChat, idUser, 245)  # todo escolher menu
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. «Contencioso\n''')
        elif opcao == 6:
            save_redis(idChat, idUser, 246)  # todo escolher menu
            return str('''Escolha uma das seguintes opções, digitando o número correspondente.
                        1. Info Portabilidade\n 2. Video Intérprete\n''')
        else:
            remove_redis(idChat,idUser)
            return None

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

    elif menu == 241:
        if opcao == 1:
            #todo scrappers ir buscar pacotes nos com televisão
            remove_redis(idChat, idUser)
            return None
        elif opcao == 2:
            #todo scrappers ir buscar telemóveis
            remove_redis(idChat, idUser)
            return None
        elif opcao == 3:
            #todo scrappers ir buscar internet fixa
            remove_redis(idChat, idUser)
            return None
        elif opcao == 4:
            #todo scrappers ir buscar internet movel
            remove_redis(idChat, idUser)
            return None
        elif opcao == 5:
            #todo scrappers ir buscar telefone
            remove_redis(idChat, idUser)
            return None
        elif opcao == 6:
            #todo scrappers ir buscar ativação de pacotes internet
            remove_redis(idChat, idUser)
            return None
        elif opcao == 7:
            # todo scrappers ir buscar apoio infotmático
            remove_redis(idChat, idUser)
            return None
        else:
            # sair
            remove_redis(idChat,idUser)
            return None

    elif menu == 242:
        if opcao == 1:
            #todo scrappers ir buscar empresas
            remove_redis(idChat, idUser)
            return None
        elif opcao == 2:
            # todo scrappers ir buscar corporate
            remove_redis(idChat, idUser)
            return None
        elif opcao == 3:
            # todo scrappers ir buscar profissionais e empresas
            remove_redis(idChat, idUser)
            return None
        elif opcao == 4:
            # todo scrappers ir buscar Particulares
            remove_redis(idChat, idUser)
            return None
        else:
            # sair
            remove_redis(idChat, idUser)
            return None
    elif menu == 243:
        if opcao == 1:
            #todo ir buscar reparacao equipamentos
            remove_redis(idChat, idUser)
            return None
        elif opcao == 2:
            # todo ir buscar reparacao equipamentos
            remove_redis(idChat, idUser)
            return None
        else:
            remove_redis(idChat, idUser)
            return None
    elif menu == 244:
        if opcao == 1:
            # todo ir buscar denuncia de pirataria
            remove_redis(idChat, idUser)
            return None
        else:
            remove_redis(idChat, idUser)
            return None
    elif menu == 245:
        if opcao == 1:
            # todo ir buscar faturas contencioso
            remove_redis(idChat, idUser)
            return None
        else:
            remove_redis(idChat, idUser)
            return None
    elif menu == 246:
        if opcao == 1:
            # todo ir buscar informações video interprete
            remove_redis(idChat, idUser)
            return None
        elif opcao == 2:
            # todo ir buscar info portabilidade
            remove_redis(idChat, idUser)
            return None
        else:
            remove_redis(idChat, idUser)
            return None

    # TODO continuar menus
    else:
        return str("Pedimos desculpa, mas algo correu mal.")
