from rules_mode import load_redis, remove_redis, save_redis

def cinema_rules(idChat, idUser, menu, msg):
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
            remove_redis(idChat, idUser)
        elif opcao == 2:
            #todo Search for movies in cinema
            remove_redis(idChat, idUser)
        elif opcao == 3:
            #todo Search for movies based on genre, producer, cast, synopsis and age restriction
            remove_redis(idChat, idUser)
        elif opcao == 4:
            #todo Search for upcoming movies
            remove_redis(idChat, idUser)
        elif opcao == 5:
            #todo Get details of movie
            remove_redis(idChat, idUser)
        elif opcao == 6:
            # todo Search for sessions of movies under a certain duration
            remove_redis(idChat, idUser)
        elif opcao == 7:
            #todo Search for the next sessions
            remove_redis(idChat, idUser)
        elif opcao == 8:
            #todo Search sessions for a given movie
            remove_redis(idChat, idUser)
        elif opcao == 9:
            #todo Search for sessions by date
            remove_redis(idChat, idUser)
        else:
            remove_redis(idChat, idUser)
            return None
