import globals #redis_db
from utils import get_content, get_loc
from regex_rules_mode import regexPrice
from pretty_print import pretty_print, ntp_answer
import json


def load_redis(idChat, idUser):
    '''Load the number of the menu that was sent to the user
    :param: chat id
    :param: user id
    '''
    aux = globals.redis_db.get(str(idChat) + str(idUser) + '_rules_mode')

    if aux:
        return int(aux)
    else:
        return 0


def remove_redis(idChat, idUser, chatData):
    '''Remove the user information on the rules mode stored in redis
    :param: chat id
    :param: user id
    :param: chatData
    '''
    if load_string(idChat, idUser, '_movie_genre'):
        remove_string(idChat, idUser, '_movie_genre')

    if load_string(idChat, idUser, '_movie_cast'):
        remove_string(idChat, idUser, '_movie_cast')

    if load_string(idChat, idUser, '_movie_producer'):
        remove_string(idChat, idUser, '_movie_producer')

    if load_string(idChat, idUser, '_movie_synopsis'):
        remove_string(idChat, idUser, '_movie_synopsis')

    if load_string(idChat, idUser, '_movie_age'):
        remove_string(idChat, idUser, '_movie_age')

    if load_string(idChat, idUser, '_search_term'):
        remove_string(idChat, idUser, '_search_term')

    if load_string(idChat, idUser, '_movie_duration'):
        remove_string(idChat, idUser, '_movie_duration')

    if load_string(idChat, idUser, '_movie_date'):
        remove_string(idChat, idUser, '_movie_date')

    if load_string(idChat, idUser, '_start_time'):
        remove_string(idChat, idUser, '_start_time')

    if load_string(idChat, idUser, '_end_time'):
        remove_string(idChat, idUser, '_end_time')

    chatData["status"] = ''
    globals.redis_db.set(idChat, json.dumps(chatData))
    globals.redis_db.delete(str(idChat) + str(idUser) + '_rules_mode')

    load_redis(idChat, idUser)


def save_redis(idChat, idUser, menu):
    '''Save the number of the menu that was sent to the user
    :param: chat id
    :param: user id
    :param: menu number
    '''
    globals.redis_db.set(str(idChat) + str(idUser) + '_rules_mode', menu)


def save_number(idChat, idUser, code, number):
    '''Save an input number from the user
    :param: chat id
    :param: user id
    :param: code to identify the number
    :param: number
    '''
    globals.redis_db.set(str(idChat) + str(idUser) + code, number.encode('utf-8'))


def load_number(idChat, idUser, code):
    '''Load an input number from the user associated with a code
    :param: chat id
    :param: user id
    :param: code to identify the number
    '''
    aux = globals.redis_db.get(str(idChat) + str(idUser) + code)

    if aux:
        return int(str(aux.decode('utf-8')))
    else:
        return None


def remove_number(idChat, idUser, code):
    '''Remove an input number from the user associated with a code
    :param: chat id
    :param: user id
    :param: code to identify the number
    '''
    globals.redis_db.delete(str(idChat) + str(idUser) + code)


def save_float(idChat, idUser, code, number):
    '''Save an input float from the user
    :param: chat id
    :param: user id
    :param: code to identify the float
    :param: float'''
    globals.redis_db.set(str(idChat) + str(idUser) + code, number)


def load_float(idChat, idUser, code):
    '''Load an input float from the user associated with a code
    :param: chat id
    :param: user id
    :param: code to identify the float
    '''
    aux = globals.redis_db.get(str(idChat) + str(idUser) + code)

    if aux:
        return float(str(aux.decode('utf-8')))
    else:
        return 0.0


def remove_float(idChat, idUser, code):
    '''Remove an input float from the user associated with a code
    :param: chat id
    :param: user id
    :param: code to identify the float
    '''
    globals.redis_db.delete(str(idChat) + str(idUser) + code)


def save_string(idChat, idUser, code, string):
    '''Save an input string from the user
    :param: chat id
    :param: user id
    :param: code to identify the string
    :param: float'''
    globals.redis_db.set(str(idChat) + str(idUser) + code, string.encode('utf-8'))


def load_string(idChat, idUser, code):
    '''Load an input string from the user associated with a code
    :param: chat id
    :param: user id
    :param: code to identify the string
    '''
    aux = globals.redis_db.get(str(idChat) + str(idUser) + code)

    if aux:
        return str(aux.decode('utf-8'))
    else:
        return None


def remove_string(idChat, idUser, code):
    '''Remove an input string from the user associated with a code
    :param: chat id
    :param: user id
    :param: code to identify the string
    '''
    globals.redis_db.delete(str(idChat) + str(idUser) + code)


def final_movies_options(idChat, idUser, chatData):
    '''Send request to Cinema Scrapper for movies with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    genre = load_string(idChat, idUser, '_movie_genre')
    cast = load_string(idChat, idUser, '_movie_cast')
    producer = load_string(idChat, idUser, '_movie_producer')
    synopsis = load_string(idChat, idUser, '_movie_synopsis')
    age = load_string(idChat, idUser, '_movie_age')

    if genre:
        aux['genre'] = genre
        remove_string(idChat, idUser, '_movie_genre')

    if cast:
        aux['cast'] = cast
        remove_string(idChat, idUser, '_movie_cast')

    if producer:
        aux['producer'] = producer
        remove_string(idChat, idUser, '_movie_producer')

    if synopsis:
        aux['synopsis'] = synopsis
        remove_string(idChat, idUser, '_movie_synopsis')

    if age:
        aux['age'] = age
        remove_string(idChat, idUser, '_movie_age')

    remove_redis(idChat, idUser, chatData)
    pretendido = get_content('/scrapper/movies/search', [], aux)
    pretty_print(idChat, '/scrapper/movies/search', pretendido, True)

    return None

def final_movies_duration(idChat, idUser, chatData):
    '''Send request to Cinema Scrapper for sessions of a movie with the chosen options and forwardthe reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')
    duration = load_string(idChat, idUser, '_movie_duration')
    date = load_string(idChat, idUser, '_movie_date')
    start = load_string(idChat, idUser, '_start_time')
    end = load_string(idChat, idUser, '_end_time')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    if duration:
        aux['duration'] = duration
        remove_string(idChat, idUser, '_movie_duration')

    if date:
        aux['date'] = date
        remove_string(idChat, idUser, '_movie_date')

    if start:
        aux['start_time'] = start
        remove_string(idChat, idUser, '_start_time')

    if end:
        aux['end_time'] = end
        remove_string(idChat, idUser, '_end_time')

    remove_redis(idChat, idUser, chatData)
    pretendido = get_content('/scrapper/sessions/by_duration', [], aux)
    pretty_print(idChat, '/scrapper/sessions/by_duration', pretendido, True)

    return None

def final_movies_duration_loc(idChat, idUser, chatData):
    '''Send request to Cinemas Scrapper for sessions of a movie with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    duration = load_string(idChat, idUser, '_movie_duration')
    date = load_string(idChat, idUser, '_movie_date')
    start = load_string(idChat, idUser, '_start_time')
    end = load_string(idChat, idUser, '_end_time')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    if 'locationParam' in chatData:
            aux['lat'] = float(chatData['locationParam']['lat'])
            aux['lon'] = float(chatData['locationParam']['lon'])
    else:
        remove_redis(idChat, idUser, chatData)
        data = {}
        data['msg'] = str("Saiu do modo de regras.")
        return data

    if duration:
        aux['duration'] = duration
        remove_string(idChat, idUser, '_movie_duration')

    if date:
        aux['date'] = date
        remove_string(idChat, idUser, '_movie_date')

    if start:
        aux['start_time'] = start
        remove_string(idChat, idUser, '_start_time')

    if end:
        aux['end_time'] = end
        remove_string(idChat, idUser, '_end_time')

    remove_redis(idChat, idUser, chatData)
    pretendido = get_content('/scrapper/sessions/by_duration', [], aux)
    pretty_print(idChat, '/scrapper/sessions/by_duration', pretendido, True)
    return None

def final_moviesNxtSessions_loc(idChat, idUser, chatData):
    '''Send request to Cinemas Scrapper for sessions of a movie with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    if 'locationParam' in chatData:
            aux['lat'] = float(chatData['locationParam']['lat'])
            aux['lon'] = float(chatData['locationParam']['lon'])
    else:
        remove_redis(idChat, idUser, chatData)
        data = {}
        data['msg'] = str("Saiu do modo de regras.")
        return data

    remove_redis(idChat, idUser, chatData)
    pretendido = get_content('/scrapper/sessions/next_sessions', [], aux)
    pretty_print(idChat, '/scrapper/sessions/next_sessions', pretendido, True)

    return None

def final_moviesNxtSessions_semloc(idChat, idUser, chatData):
    '''Send request to Cinemas Scrapper for sessions of a movie with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    remove_redis(idChat, idUser, chatData)
    return get_content('/scrapper/sessions/next_sessions', [], aux)

def final_movies_sessoesDate_loc(idChat, idUser, chatData):
    '''Send request to Cinemas Scrapper for session of a movie with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    date = load_string(idChat, idUser, '_date')
    start = load_string(idChat, idUser, '_start_time')
    end = load_string(idChat, idUser, '_end_time')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    if 'locationParam' in chatData:
            aux['lat'] = float(chatData['locationParam']['lat'])
            aux['lon'] = float(chatData['locationParam']['lon'])
    else:
        remove_redis(idChat, idUser, chatData)
        data = {}
        data['msg'] = str("Saiu do modo de regras.")
        return data

    if date:
        aux['date'] = date
        remove_string(idChat, idUser, '_date')

    if start:
        aux['start_time'] = start
        remove_string(idChat, idUser, '_start_time')

    if end:
        aux['end_time'] = end
        remove_string(idChat, idUser, '_end_time')

    remove_redis(idChat, idUser, chatData)
    pretendido = get_content('/scrapper/sessions/by_date', [], aux)
    pretty_print(idChat, '/scrapper/sessions/by_date', pretendido, True)
    print("MOVIES SESSOES LOC")
    print(pretendido)

    return None


def final_movies_sessoesDate(idChat, idUser, chatData):
    '''Send request to Cinemas Scrapper for session of a movie with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    date = load_string(idChat, idUser, '_date')
    start = load_string(idChat, idUser, '_start_time')
    end = load_string(idChat, idUser, '_end_time')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    if date:
        aux['date'] = date
        remove_string(idChat, idUser, '_date')

    if start:
        aux['start_time'] = start
        remove_string(idChat, idUser, '_start_time')

    if end:
        aux['end_time'] = end
        remove_string(idChat, idUser, '_end_time')

    remove_redis(idChat, idUser, chatData)
    pretendido = get_content('/scrapper/sessions/by_date', [], aux)
    pretty_print(idChat, '/scrapper/sessions/by_date', pretendido, True)
    print("MOVIES SESSOES")
    print(pretendido)

    return None


def final_movies_bymovie_loc(idChat, idUser, chatData):
    '''Send request to Cinemas Scrapper for session of a movie with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    movie = load_string(idChat, idUser, '_movie_name')
    date = load_string(idChat, idUser, '_date')
    start = load_string(idChat, idUser, '_start_time')
    end = load_string(idChat, idUser, '_end_time')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    if chatData['locationParam'] is not None:
        print("LOCALIZAÇÃO")
        print(chatData['locationParam'])
        aux['lat'] = float(chatData['locationParam']['lat'])
        aux['lon'] = float(chatData['locationParam']['lon'])

    if movie:
        aux['movie'] = movie
        remove_string(idChat, idUser, '_movie_name')

    if date:
        aux['date'] = date
        remove_string(idChat, idUser, '_date')

    if start:
        aux['start_time'] = start
        remove_string(idChat, idUser, '_start_time')

    if end:
        aux['end_time'] = end
        remove_string(idChat, idUser, '_end_time')

    remove_redis(idChat, idUser, chatData)
    pretendido = get_content('/scrapper/sessions/by_movie', [], aux)
    pretty_print(idChat, '/scrapper/sessions/by_movie', pretendido, True)
    print("MOVIES BY MOVIE LOC")
    print(pretendido)
    return None


def final_movies_bymovie(idChat, idUser, chatData):
    '''Send request to Cinemas Scrapper for session of a movie with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    movie = load_string(idChat, idUser, '_movie_name')
    date = load_string(idChat, idUser, '_date')
    start = load_string(idChat, idUser, '_start_time')
    end = load_string(idChat, idUser, '_end_time')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    if movie:
        aux['movie'] = movie
        remove_string(idChat, idUser, '_movie_name')

    if date:
        aux['date'] = date
        remove_string(idChat, idUser, '_date')

    if start:
        aux['start_time'] = start
        remove_string(idChat, idUser, '_start_time')

    if end:
        aux['end_time'] = end
        remove_string(idChat, idUser, '_end_time')

    remove_redis(idChat, idUser, chatData)
    pretendido = get_content('/scrapper/sessions/by_movie', [], aux)
    pretty_print(idChat, '/scrapper/sessions/by_movie', pretendido, True)
    return None


def final_packages(idChat, idUser):
    '''Send request to FS Scrapper for packages with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    tipo = load_string(idChat, idUser, '_package_type')
    servico = load_string(idChat, idUser, '_package_service')
    preco = load_string(idChat, idUser, '_package_price')

    if tipo:
        aux['type'] = tipo
        aux['type'] = tipo
        remove_string(idChat, idUser, '_package_type')

    if servico:
        aux['service'] = servico
        remove_string(idChat, idUser, '_package_service')

    if preco:
        aux['min'] = load_float(idChat, idUser, '_min_value')
        aux['max'] = load_float(idChat, idUser, '_max_value')
        remove_string(idChat, idUser, '_package_price')
        remove_float(idChat, idUser, '_min_value')
        remove_float(idChat, idUser, '_max_value')

    pretendido = get_content('/fs_scrapper/packages', [], aux)
    pretty_print(idChat, '/fs_scrapper/packages', pretendido, False)

    return None


def final_phones(idChat, idUser):
    '''Send request to FS Scrapper for phones with the chosen options and forward the reply to user
    :param: chat id
    :param: user id
    '''
    aux = {}
    promo = load_string(idChat, idUser, '_phones_Promo_')
    newPhones = load_string(idChat, idUser, '_new_phones_')
    brand = load_string(idChat, idUser, '_phones_brand_')
    points = load_string(idChat, idUser, '_points_')
    prest = load_string(idChat, idUser, '_prest_')
    priceLimit = load_string(idChat, idUser, '_priceLimit_')
    ofer = load_string(idChat, idUser, '_phones_ofer')

    if priceLimit:
        aux['min'] = load_float(idChat, idUser, '_min_value_')
        aux['max'] = load_float(idChat, idUser, '_max_value_')
        remove_string(idChat, idUser, '_priceLimit_')
        remove_float(idChat, idUser, '_min_value_')
        remove_float(idChat, idUser, '_max_value_')
    if brand:
        aux['brand'] = brand
        print(brand)
        remove_string(idChat, idUser, '_phones_brand_')
    if promo:
        aux['promo'] = True
        remove_string(idChat, idUser, '_phones_Promo_')
    if points:
        aux['points'] = True
        remove_string(idChat, idUser, '_points_')
    if prest:
        aux['prest'] = True
        remove_string(idChat, idUser, '_prest_')
    if newPhones:
        aux['new'] = True
        remove_string(idChat, idUser, '_new_phones_')
    if ofer:
        aux['ofer'] = True
        remove_string(idChat, idUser, '_phones_ofer')

    pretendido = get_content('/fs_scrapper/phones', [], aux)
    pretty_print(idChat, '/fs_scrapper/phones', pretendido, False)

    return None


def get_response_rules(idChat, idUser, msg, name, chatData):
    '''Send the first menu of the rules mode to the user and identify the correct method to process the received message
    :param: chat id
    :param: user id
    :param: messagem received from user
    :param: user name
    :param: chatData
    '''
    menu = load_redis(idChat, idUser)

    if menu == 0:
        save_redis(idChat, idUser, 1)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'Cinemas ou sessões','callback_data': '1'}],
                [{'text': 'Tarifários ou pacotes','callback_data': '2'}],
                [{'text': 'Compra de telemóveis','callback_data': '3'}],
                [{'text': 'Lojas da NOS','callback_data': '4'}],
                [{'text': 'Linhas de apoio','callback_data': '5'}],
                [{'text': 'Problemas técnicos','callback_data': '6'}],
                [{'text': 'Sair','callback_data': '7'}]
            ]
        }
        data = {}
        data['msg'] = 'Escolha uma das opções apresentadas.'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 1:
        opcao = int(msg)

        if opcao == 1:
            resposta = cinema_rules(idChat, idUser, opcao, msg, chatData)
            return resposta

        elif opcao == 2 or opcao == 3 or opcao == 4 or opcao == 5:
            resposta = fs_rules(idChat, idUser, opcao, msg, chatData)
            return resposta

        elif opcao == 6:
            chatData["status"] == "modo problemas"
            globals.redis_db.set(idChat, json.dumps(chatData))
            ntp_answer(idChat, msg, False)

        elif opcao == 7:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif 10 < menu < 20 or 100 < menu < 200:
        resposta = cinema_rules(idChat, idUser, menu, msg, chatData)
        return resposta

    elif 20 < menu < 30 or 200 < menu < 300:
        resposta = fs_rules(idChat, idUser, menu, msg, chatData)
        return resposta

    else:
        data = {}
        data['msg'] = str("Pedimos desculpa, mas algo correu mal.")
        return data


def cinema_rules(idChat, idUser, menu, msg, chatData):
    '''Deal with cinema related steps of the rules mode, process user messages and send the following step
    :param: chat id
    :param: user id
    :param: number of the menu sent to user
    :param: messagem received from user
    :param: chatData
    '''
    try:
        opcao = int(msg)
    except ValueError:
        opcao = -1

    if menu == 1:
        save_redis(idChat, idUser, 11)
        reply_markup={
                'inline_keyboard': [
            [{'text': 'Procurar cinemas','callback_data': '1'}],
            [{'text': 'Filmes em sessão ','callback_data': '2'}],
            [{'text': 'Filmes específicos','callback_data': '3'}],
            [{'text': 'Próximas estreias','callback_data': '4'}],
            [{'text': 'Informação de um filme','callback_data': '5'}],
            [{'text': 'Sessões com certa duração','callback_data': '6'}],
            [{'text': 'Proximas sessões','callback_data': '7'}],
            [{'text': 'Sessões de um filme','callback_data': '8'}],
            [{'text': 'Sessões por data','callback_data': '9'}],
            [{'text': 'Sair','callback_data': '10'}]
                ]
        }

        data = {}
        data['msg'] = 'Escolha uma das seguintes opções.'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 11:
        data = {}
        if opcao == 1:
            save_redis(idChat, idUser, 12)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Cinema em específico ','callback_data': '1'}],
                    [{'text': 'Perto de localização','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2:
            save_redis(idChat, idUser, 13)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Cinema em específico ','callback_data': '1'}],
                    [{'text': 'Perto de localização','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 3:
            save_redis(idChat, idUser, 14)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Genero','callback_data': '1'}],
                    [{'text': 'Cast','callback_data': '2'}],
                    [{'text': 'Produtor','callback_data': '3'}],
                    [{'text': 'Sinopse','callback_data': '4'}],
                    [{'text': 'Faixa etária','callback_data': '5'}],
                    [{'text': 'Sair','callback_data': '6'}]
                ]
            }
            data['msg'] = 'Escolha o que pretende especificar.'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 4: # Apresentar próximas estreias
            remove_redis(idChat, idUser, chatData)
            requerido = get_content('/scrapper/movies/releases', [], {})
            pretty_print(idChat, '/scrapper/movies/releases', requerido, True)
            return None

        elif opcao == 5:
            save_redis(idChat, idUser, 15)
            data['msg'] = str('''Especifique o filme que pretende obter infomações sobre.''')
            return data

        elif opcao == 6:
            save_redis(idChat, idUser, 16)
            data['msg'] = str('''Especifique a duração do filme que pretende, em minutos.''')
            return data

        elif opcao == 7:
            save_redis(idChat, idUser, 17)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data['msg'] = 'Pretende especificar algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 8:
            save_redis(idChat, idUser, 18)
            data['msg'] = str('''Especifique o nome do filme.''')
            return data

        elif opcao == 9:
            save_redis(idChat, idUser, 19)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data['msg'] = 'Pretende especificar algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 10:
            remove_redis(idChat, idUser, chatData)
            data['msg'] = str('''Saiu do modo de regras.''')
            return data

    elif menu == 19:
        if opcao == 1:
            save_redis(idChat, idUser, 191)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Termo de pesquisa','callback_data': '1'}],
                    [{'text': 'Usar localização','callback_data': '2'}],
                    [{'text': 'Data (ano-mês-dia)','callback_data': '3'}],
                    [{'text': 'Hora inicio das sessões','callback_data': '4'}],
                    [{'text': 'Hora fim das sessões','callback_data': '5'}],
                    [{'text': 'Sair','callback_data': '6'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções'
            data['menu'] = json.dumps(reply_markup)
            return data

        if opcao == 2: # procurar sessoes por filme
            if chatData['locationParam'] is None:
                final_movies_bymovie(idChat, idUser, chatData)
            else:
                final_movies_bymovie_loc(idChat, idUser, chatData)
            return None

    elif menu == 190:
        if opcao == 1:
            save_redis(idChat, idUser, 191)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Termo de pesquisa','callback_data': '1'}],
                    [{'text': 'Usar localização','callback_data': '2'}],
                    [{'text': 'Data (ano-mês-dia)','callback_data': '3'}],
                    [{'text': 'Hora inicio das sessões','callback_data': '4'}],
                    [{'text': 'Hora fim das sessões','callback_data': '5'}],
                    [{'text': 'Sair','callback_data': '6'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções para especificar'
            data['menu'] = json.dumps(reply_markup)
            return data

        if opcao == 2: # procurar sessoes por filme
            final_movies_bymovie_loc(idChat, idUser, chatData)
            #final_movies_sessoes_loc(idChat, idUser, chatData)
            remove_redis(idChat, idUser, chatData)
            return None

    elif menu == 191:
        if opcao == 1:
            save_redis(idChat, idUser, 199)
            data = {}
            data['msg'] = str('''Escreva termo de pesquisa para um cinema''')
            return data

        if opcao == 2: # procurar sessoes por filme
            save_redis(idChat, idUser, 190)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar mais algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

        if opcao == 3: # procurar sessoes por filme
            save_redis(idChat, idUser, 197)
            data = {}
            data['msg'] = str('''Indique a data (ano-mês-dia)''')
            return data

        if opcao == 4: # procurar sessoes por filme
            save_redis(idChat, idUser, 196)
            data = {}
            data['msg'] = str('''Especifique limite para início das sessões''')
            return data

        if opcao == 5: # procurar sessoes por filme
            save_redis(idChat, idUser, 195)
            data = {}
            data['msg'] = str('''Especifique limite para fim das sessões''')
            return data

    elif menu == 199:
        save_string(idChat, idUser, '_search_term', msg)
        print("Search terM")
        print(msg)
        save_redis(idChat, idUser, 19)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 198:
        save_redis(idChat, idUser, 190)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 197:
        save_string(idChat, idUser, '_date', msg)
        save_redis(idChat, idUser, 19)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 196:
        save_string(idChat, idUser, '_start_time', msg)
        save_redis(idChat, idUser, 19)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 195:
        save_string(idChat, idUser, '_end_time', msg)
        save_redis(idChat, idUser, 19)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 18:
        save_string(idChat, idUser, '_movie_name', msg)
        save_redis(idChat, idUser, 180)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 180:
        if opcao == 1:
            save_redis(idChat, idUser, 181)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Termo de pesquisa','callback_data': '1'}],
                    [{'text': 'Usar localização','callback_data': '2'}],
                    [{'text': 'Data (ano-mês-dia)','callback_data': '3'}],
                    [{'text': 'Hora inicio das sessões','callback_data': '4'}],
                    [{'text': 'Hora fim das sessões','callback_data': '5'}],
                    [{'text': 'Sair','callback_data': '6'}],
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções para especificar'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: # procurar sessoes por filme
            final_movies_bymovie(idChat, idUser, chatData)
            return None

        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str('''Saiu do modo de regras.''')
            return data

    elif menu == 130:
            save_redis(idChat, idUser, 190)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar mais algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

    elif menu == 181:
        if opcao == 1:
            save_redis(idChat, idUser, 189)
            data = {}
            data['msg'] = str('''Escreva termo de pesquisa para um cinema''')
            return data

        elif opcao == 2: # procurar sessoes por filme
            chatData['previous_state'] = 'modo regras'
            get_loc(idChat)
            save_redis(idChat, idUser, 130)
            data = {}
            data['msg'] = str('''Para prosseguir precisamos do seu consentimento, por favor prima o botão se concordar.''')
            return data

        elif opcao == 3: # procurar sessoes por filme
            save_redis(idChat, idUser, 187)
            data = {}
            data['msg'] = str("Indique a data (ano-mês-dia)")
            return data

        elif opcao == 4: # procurar sessoes por filme
            save_redis(idChat, idUser, 186)
            data = {}
            data['msg'] = str("Especifique limite para início das sessões")
            return data

        elif opcao == 5: # procurar sessoes por filme
            save_redis(idChat, idUser, 185)
            data = {}
            data['msg'] = str("Especifique limite para fim das sessões")
            return data

        elif opcao == 6:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str('''Saiu do modo de regras.''')
            return data

    elif menu == 189:
        save_string(idChat, idUser, '_search_term', 'all')
        save_redis(idChat, idUser, 180)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 131:
            save_redis(idChat, idUser, 190)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar mais algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

    elif menu == 188:
        #save lat e lon
        chatData['previous_state'] = 'modo regras'
        get_loc(idChat)
        save_redis(idChat, idUser, 131)

    elif menu == 187:
        save_string(idChat, idUser, '_date', msg)
        save_redis(idChat, idUser, 180)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 186:
        save_string(idChat, idUser, '_inicio', msg)
        save_redis(idChat, idUser, 180)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 185:
        save_string(idChat, idUser, '_fim', msg)
        save_redis(idChat, idUser, 180)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 17:
        if opcao == 1: # perguntar por termos
            save_redis(idChat, idUser, 108)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Termo de procura','callback_data': '1'}],
                    [{'text': 'Usar localização','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar mais algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: # fazer a pesquisa sem localização
            final_moviesNxtSessions_semloc(idChat, idUser, chatData)
            #remove_redis(idChat, idUser, chatData)
            return None

    elif menu == 108:
        if opcao == 1:
            save_redis(idChat, idUser, 169)
            data = {}
            data['msg'] = str('''Especifique termo de procura por cinema''')
            return data
        elif opcao == 2:
            save_redis(idChat, idUser, 110)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar mais algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str('''Saiu do modo de regras.''')
            return data

    elif menu == 169:
        save_string(idChat, idUser, '_search_term', msg)
        save_redis(idChat, idUser, 17)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 168:
        save_redis(idChat, idUser, 110)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 110:
        if opcao == 1:
            save_redis(idChat, idUser, 139)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Termo de procura','callback_data': '1'}],
                    [{'text': 'Usar localização','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções para especificar.'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: # fazer a pesquisa com localização
            final_moviesNxtSessions_loc(idChat, idUser, chatData)
            #remove_redis(idChat, idUser, chatData)
            return None

    elif menu == 139:
        data = {}
        if opcao == 1:
            save_redis(idChat, idUser, 168)
            data['msg'] = str('''Especifique termo de procura por cinema''')
            return data
        elif opcao == 1:
            save_redis(idChat, idUser, 110)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data['msg'] = 'Pretende especificar mais algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

    elif menu == 16:
        save_string(idChat, idUser, '_movie_duration', msg)
        save_redis(idChat, idUser, 107)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 107:
        if opcao == 1:
            save_redis(idChat, idUser, 158)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Termo de pesquisa','callback_data': '1'}],
                    [{'text': 'Usar localização','callback_data': '2'}],
                    [{'text': 'Data (ano-mês-dia)','callback_data': '3'}],
                    [{'text': 'Hora inicio das sessões','callback_data': '4'}],
                    [{'text': 'Hora fim das sessões','callback_data': '5'}],
                    [{'text': 'Sair','callback_data': '6'}],
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções para especificar'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: #fazer pesquisa de duração de filme
            final_movies_duration(idChat, idUser, chatData)
            #remove_redis(idChat, idUser, chatData)
            return None

    elif menu == 132:
            save_redis(idChat, idUser, 159)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar mais algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

    elif menu == 158:
        if opcao == 1:
            save_redis(idChat, idUser, 149)
            data = {}
            data['msg'] = str('''Escreva termo de pesquisa para um cinema''')
            return data

        elif opcao == 2: # procurar sessoes por filme
            #save lat e lon
            chatData['previous_state'] = 'modo regras'
            get_loc(idChat)
            save_redis(idChat, idUser, 132)
            data = {}
            data['msg'] = str('''Para prosseguir precisamos do seu consentimento, por favor prima o botão se concordar.''')
            return data

        elif opcao == 3: # procurar sessoes por filme
            save_redis(idChat, idUser, 147)
            data = {}
            data['msg'] = str('''Indique a data (ano-mês-dia)''')
            return data

        elif opcao == 4: # procurar sessoes por filme
            save_redis(idChat, idUser, 146)
            data = {}
            data['msg'] = str('''Especifique limite para início das sessões''')
            return data

        elif opcao == 5: # procurar sessoes por filme
            save_redis(idChat, idUser, 145)
            data = {}
            data['msg'] = str('''Especifique limite para fim das sessões''')
            return data

        elif opcao == 6:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str('''Saiu do modo de regras.''')
            return data

    elif menu == 149:
        save_string(idChat, idUser, '_search_term', msg)
        save_redis(idChat, idUser, 180)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 133:
            save_redis(idChat, idUser, 159)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar mais algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

    elif menu == 148:
        #save lat e lon
        chatData['previous_state'] = 'modo regras'
        get_loc(idChat)
        save_redis(idChat, idUser, 133)
        data = {}
        data['msg'] = str('''Para prosseguir precisamos do seu consentimento, por favor prima o botão se concordar.''')
        return data

    elif menu == 147:
        save_string(idChat, idUser, '_date', msg)
        save_redis(idChat, idUser, 107)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 146:
        save_string(idChat, idUser, '_inicio', msg)
        save_redis(idChat, idUser, 107)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 145:
        save_string(idChat, idUser, '_fim', msg)
        save_redis(idChat, idUser, 107)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 159:
        if opcao == 1:
            save_redis(idChat, idUser, 158)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Termo de pesquisa','callback_data': '1'}],
                    [{'text': 'Usar localização','callback_data': '2'}],
                    [{'text': 'Data (ano-mês-dia)','callback_data': '3'}],
                    [{'text': 'Hora inicio das sessões','callback_data': '4'}],
                    [{'text': 'Hora fim das sessões','callback_data': '5'}],
                    [{'text': 'Sair','callback_data': '6'}],
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções para especificar'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: #fazer pesquisa de duração de filme
            final_movies_duration_loc(idChat, idUser, chatData)
            remove_redis(idChat, idUser, chatData)
            return None

    elif menu == 15: # obter info do filme
        aux = {}
        aux['movie'] = msg
        remove_redis(idChat, idUser, chatData)
        requerido = get_content('/scrapper/movies/details', [], aux)
        pretty_print(idChat, '/scrapper/movies/details', requerido, True)
        return None

    elif menu == 14:
        if opcao == 1:
            save_redis(idChat, idUser, 179)
            data = {}
            data['msg'] = str('''Especifique que tipo de género pretende.''')
            return data

        elif opcao == 2:
            save_redis(idChat, idUser, 178)
            data = {}
            data['msg'] = str('''Especifique o cast, separando cada nome por vírgula.''')
            return data

        elif opcao == 3:
            save_redis(idChat, idUser, 177)
            data = {}
            data['msg'] = str('''Especifique um produtor.''')
            return data

        elif opcao == 4:
            save_redis(idChat, idUser, 176)
            data = {}
            data['msg'] = str('''Especifique expressões para procurar na sinopse''')
            return data

        elif opcao == 5:
            save_redis(idChat, idUser, 175)
            data = {}
            data['msg'] = str('''Especifique faixa etária''')
            return data

        elif opcao == 6:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str('''Saiu do modo de regras.''')
            return data

    elif menu == 179:
        save_string(idChat, idUser, '_movie_genre', msg)
        save_redis(idChat, idUser, 106)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 178:
        save_string(idChat, idUser, '_movie_cast', msg)
        save_redis(idChat, idUser, 106)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 177:
        save_string(idChat, idUser, '_movie_producer', msg)
        save_redis(idChat, idUser, 106)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 176:
        save_string(idChat, idUser, '_movie_synopsis', msg)
        save_redis(idChat, idUser, 106)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 175:
        save_string(idChat, idUser, '_movie_age', msg)
        save_redis(idChat, idUser, 106)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
            ]
        }
        data = {}
        data['msg'] = 'Pretende especificar mais algum parametro?'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 106:
        if opcao == 1: # apresentar opções outra vez
            save_redis(idChat, idUser, 14)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Genero','callback_data': '1'}],
                    [{'text': 'Cast','callback_data': '2'}],
                    [{'text': 'Produtor','callback_data': '3'}],
                    [{'text': 'Sinopse','callback_data': '4'}],
                    [{'text': 'Faixa etária','callback_data': '5'}],
                    [{'text': 'Sair','callback_data': '6'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha o que pretende especificar.'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: # fazer a pesquisa
            final_movies_options(idChat, idUser, chatData)
            #remove_redis(idChat, idUser, chatData)
            return None

    elif menu == 134:
            if 'locationParam' in chatData:
                aux = {}
                aux['lat'] = float(chatData['locationParam']['lat'])
                aux['lon'] = float(chatData['locationParam']['lon'])
                requerido = get_content('/scrapper/movies/by_cinema', [], aux)
                pretty_print(idChat, '/scrapper/movies/by_cinema', requerido, True)
                remove_redis(idChat, idUser, chatData)
                return None
            else:
                remove_redis(idChat, idUser, chatData)
                data = {}
                data['msg'] = str("Saiu do modo de regras.")
                return data
    elif menu == 13:
        data = {}
        if opcao == 1: #procurar cinemas com query
            save_redis(idChat, idUser, 102)
            data['msg'] = str('''Insira uma expressão para procurar o cinema''')
            return data

        elif opcao == 2: #procurar cinemas com lat e long
            chatData['previous_state'] = 'modo regras'
            get_loc(idChat)
            save_redis(idChat, idUser, 134)
            data['msg'] = str('''Para prosseguir precisamos do seu consentimento, por favor prima o botão se concordar.''')
            return data

        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data['msg'] = str('''Saiu do modo de regras.''')
            return data

    elif menu == 135:
        if 'locationParam' in chatData:
            aux = {}
            aux['lat'] = float(chatData['locationParam']['lat'])
            aux['lon'] = float(chatData['locationParam']['lon'])
            requerido = get_content('/scrapper/cinemas/search', [], aux)
            pretty_print(idChat, '/scrapper/cinemas/search', requerido, True)
            remove_redis(idChat, idUser, chatData)
            return None
        else:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data
    elif menu == 12:
        data = {}
        if opcao == 1: #procurar cinemas com query
            save_redis(idChat, idUser, 101)
            data['msg'] = str('''Insira uma expressão para procurar o cinema''')
            return data

        elif opcao == 2: #procurar cinemas com lat e long
            chatData['previous_state'] = 'modo regras'
            get_loc(idChat)
            save_redis(idChat, idUser, 135)
            data['msg'] = str('''Para prosseguir precisamos do seu consentimento, por favor prima o botão se concordar.''')
            return data

        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data['msg'] = str('''Saiu do modo de regras.''')
            return data

    elif menu == 101: #procurar cinemas com query
        remove_redis(idChat, idUser, chatData)
        aux = {}
        aux['search_term'] = msg
        requerido = get_content('/scrapper/cinemas/search', [], aux)
        pretty_print(idChat, '/scrapper/cinemas/search', requerido, True)
        return None

    elif menu == 102: #procurar cinemas com query
        remove_redis(idChat, idUser, chatData)
        aux = {}
        aux['search_term'] = msg
        requerido = get_content('/scrapper/movies/by_cinema', [], aux)
        pretty_print(idChat, '/scrapper/movies/by_cinema', requerido, True)
        return None

def fs_rules(idChat, idUser, menu, msg, chatData):
    '''Deal with FS related steps of the rules mode, process user messages and send the following step
    :param: chat id
    :param: user id
    :param: number of the menu sent to user
    :param: messagem received from user
    :param: chatData
    '''
    try:
        opcao = int(msg)
    except ValueError:
        opcao = -1

    if menu == 2:
        save_redis(idChat, idUser, 21)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'Tarifários WTF','callback_data': '1'}],
                [{'text': 'Pacotes','callback_data': '2'}],
                [{'text': 'Sair','callback_data': '3'}]
            ]
        }
        data = {}
        data['msg'] = 'Escolha uma das opções apresentadas.'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 3:
        save_redis(idChat, idUser, 22)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'Modelo de telemóvel','callback_data': '1'}],
                [{'text': 'Pesquisa sobre telemóveis','callback_data': '2'}],
                [{'text': 'Top telemóveis mais vistos','callback_data': '3'}],
                [{'text': 'Sair','callback_data': '4'}]
            ]
        }
        data = {}
        data['msg'] = 'Escolha uma das opções apresentadas.'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 4:
        save_redis(idChat, idUser, 23)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'Indicar zona prentendida','callback_data': '1'}],
                [{'text': 'Lojas perto de si','callback_data': '2'}],
                [{'text': 'Sair','callback_data': '3'}]
            ]
        }
        data = {}
        data['msg'] = 'Escolha uma das opções apresentadas.'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 5:
        save_redis(idChat, idUser, 24)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'Especificar assunto','callback_data': '1'}],
                [{'text': 'Todas as linhas de apoio','callback_data': '2'}],
                [{'text': 'Sair','callback_data': '3'}]
            ]
        }
        data = {}
        data['msg'] = 'Escolha uma das opções apresentadas.'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 21:
        if opcao == 1:
            save_redis(idChat, idUser, 25)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Todos os tarifários WTF','callback_data': '1'}],
                    [{'text': 'Tarifários por nome','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções apresentadas.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 2:
            save_redis(idChat, idUser, 26)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Indicar nome de pacote','callback_data': '1'}],
                    [{'text': 'Pesquisa sobre pacotes','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções apresentadas.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 22:
        if opcao == 1:
            save_redis(idChat, idUser, 221)
            data = {}
            data['msg'] = str('''Indique o nome do modelo que pretende.''')
            return data
        elif opcao == 2:
            save_redis(idChat, idUser, 222)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Especificar marca','callback_data': '1'}],
                    [{'text': 'Modelos recentes','callback_data': '2'}],
                    [{'text': 'Promoções','callback_data': '3'}],
                    [{'text': 'Telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'Definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'Pagamento a prestações','callback_data': '6'}],
                    [{'text': 'Pagamento com pontos','callback_data': '7'}],
                    [{'text': 'Apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'Sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['top'] = True
            requerido = get_content('/fs_scrapper/phones', [], aux)
            pretty_print(idChat, '/fs_scrapper/phones', requerido, True)
            return None
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 221:
        remove_redis(idChat, idUser, chatData)
        aux = {}
        aux['brand'] = msg
        requerido = get_content('/fs_scrapper/phones', [], aux)
        pretty_print(idChat, '/fs_scrapper/phones', requerido, True)
        return None

    elif menu == 222:
        if opcao == 1:
            save_redis(idChat, idUser, 223)
            data = {}
            data['msg'] = str('''Indique a marca que pretende.''')
            return data
        elif opcao == 2:
            save_string(idChat, idUser, '_new_phones_', 'defined')
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Especificar marca','callback_data': '1'}],
                    [{'text': 'Modelos recentes','callback_data': '2'}],
                    [{'text': 'Promoções','callback_data': '3'}],
                    [{'text': 'Telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'Definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'Pagamento a prestações','callback_data': '6'}],
                    [{'text': 'Pagamento com pontos','callback_data': '7'}],
                    [{'text': 'Apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'Sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            save_string(idChat, idUser, '_phones_Promo_', 'defined')
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Especificar marca','callback_data': '1'}],
                    [{'text': 'Modelos recentes','callback_data': '2'}],
                    [{'text': 'Promoções','callback_data': '3'}],
                    [{'text': 'Telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'Definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'Pagamento a prestações','callback_data': '6'}],
                    [{'text': 'Pagamento com pontos','callback_data': '7'}],
                    [{'text': 'Apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'Sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 4:
            save_string(idChat, idUser, '_phones_ofer', 'defined')
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Especificar marca','callback_data': '1'}],
                    [{'text': 'Modelos recentes','callback_data': '2'}],
                    [{'text': 'Promoções','callback_data': '3'}],
                    [{'text': 'Telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'Definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'Pagamento a prestações','callback_data': '6'}],
                    [{'text': 'Pagamento com pontos','callback_data': '7'}],
                    [{'text': 'Apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'Sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 5:
            save_redis(idChat, idUser, 224)
            save_string(idChat, idUser, '_priceLimit_', 'defined')
            data = {}
            data['msg'] = str('''Indique o valor mínimo.''')
            return data
        elif opcao == 6:
            save_string(idChat, idUser, '_prest_', 'defined')
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Especificar marca','callback_data': '1'}],
                    [{'text': 'Modelos recentes','callback_data': '2'}],
                    [{'text': 'Promoções','callback_data': '3'}],
                    [{'text': 'Telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'Definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'Pagamento a prestações','callback_data': '6'}],
                    [{'text': 'Pagamento com pontos','callback_data': '7'}],
                    [{'text': 'Apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'Sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 7:
            save_string(idChat, idUser, '_points_', 'defined')
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Especificar marca','callback_data': '1'}],
                    [{'text': 'Modelos recentes','callback_data': '2'}],
                    [{'text': 'Promoções','callback_data': '3'}],
                    [{'text': 'Telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'Definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'Pagamento a prestações','callback_data': '6'}],
                    [{'text': 'Pagamento com pontos','callback_data': '7'}],
                    [{'text': 'Apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'Sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 8:
            remove_redis(idChat, idUser, chatData)
            final_phones(idChat, idUser)
            return None
        elif opcao == 9:
            remove_string(idChat, idUser, '_phones_brand_')
            remove_string(idChat, idUser, '_new_phones_')
            remove_string(idChat, idUser, '_priceLimit_')
            remove_string(idChat, idUser, '_phones_Promo_')
            remove_string(idChat, idUser, '_points_')
            remove_string(idChat, idUser, '_prest_')
            remove_string(idChat, idUser, '_phones_ofer')
            remove_float(idChat, idUser, '_min_value_')
            remove_float(idChat, idUser, '_max_value_')
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 223:
        save_string(idChat, idUser, '_phones_brand_', msg)
        save_redis(idChat, idUser, 222)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'Especificar marca','callback_data': '1'}],
                [{'text': 'Modelos recentes','callback_data': '2'}],
                [{'text': 'Promoções','callback_data': '3'}],
                [{'text': 'Telemóveis com ofertas','callback_data': '4'}],
                [{'text': 'Definir intervalo de preços','callback_data': '5'}],
                [{'text': 'Pagamento a prestações','callback_data': '6'}],
                [{'text': 'Pagamento com pontos','callback_data': '7'}],
                [{'text': 'Apresentar resultados da pesquisa','callback_data': '8'}],
                [{'text': 'Sair','callback_data': '9'}]
            ]
        }
        data = {}
        data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 224:
        valorMin = regexPrice(msg)
        save_float(idChat, idUser, '_min_value_', valorMin)
        save_redis(idChat, idUser, 225)
        data = {}
        data['msg'] = str('''Indique o valor máximo que procura.''')
        return data

    elif menu == 225:
        valorMax = regexPrice(msg)
        save_float(idChat, idUser, '_max_value_', valorMax)
        save_redis(idChat, idUser, 222)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'Especificar marca','callback_data': '1'}],
                [{'text': 'Modelos recentes','callback_data': '2'}],
                [{'text': 'Promoções','callback_data': '3'}],
                [{'text': 'Telemóveis com ofertas','callback_data': '4'}],
                [{'text': 'Definir intervalo de preços','callback_data': '5'}],
                [{'text': 'Pagamento a prestações','callback_data': '6'}],
                [{'text': 'Pagamento com pontos','callback_data': '7'}],
                [{'text': 'Apresentar resultados da pesquisa','callback_data': '8'}],
                [{'text': 'Sair','callback_data': '9'}]
            ]
        }
        data = {}
        data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 23:
        if opcao == 1:
            save_redis(idChat, idUser, 231)
            data = {}
            data['msg'] = str('''Indique uma zona ou morada para a qual procura lojas NOS.''')
            return data
        elif opcao == 2:
            save_redis(idChat, idUser, 232)
            chatData['previous_state'] = 'modo regras'
            get_loc(idChat)
            data = {}
            data['msg'] = str('''Para prosseguir precisamos do seu consentimento, por favor prima o botão se concordar.''')
            return data
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 24:
        if opcao == 1:
            save_redis(idChat, idUser, 241)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Serviços NOS','callback_data': '1'}],
                    [{'text': 'Entidades','callback_data': '2'}],
                    [{'text': 'Equipamentos NOS','callback_data': '3'}],
                    [{'text': 'Denúncia fraude/pirataria','callback_data': '4'}],
                    [{'text': 'Faturas contencioso','callback_data': '5'}],
                    [{'text': 'Informações','callback_data': '6'}],
                    [{'text': 'Sair','callback_data': '7'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        if opcao == 2:
            remove_redis(idChat, idUser, chatData)
            requerido = get_content('/fs_scrapper/linhas_apoio', [], {})
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, False)
            return None
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 25:
        if opcao == 1:
            remove_redis(idChat, idUser, chatData)
            requerido = get_content('/fs_scrapper/wtf', [], {})
            pretty_print(idChat, '/fs_scrapper/wtf', requerido, True)
            return None
        elif opcao == 2:
            save_redis(idChat, idUser, 251)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'WTF 1GB','callback_data': '1'},{'text': 'WTF 5GB','callback_data': '2'}],
                    [{'text': 'WTF 10GB','callback_data': '3'},{'text': 'sair','callback_data': '4'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 26:
        if opcao == 1:
            save_redis(idChat, idUser, 261)
            data = {}
            data['msg'] = str('''Indique o nome do pacote pretendido.''')
            return data
        elif opcao == 2:
            save_redis(idChat, idUser, 262)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Pacotes fibra','callback_data': '1'}],
                    [{'text': 'Pacotes satélite','callback_data': '2'}],
                    [{'text': 'Todos os tipos de pacotes','callback_data': '3'}],
                    [{'text': 'Sair','callback_data': '4'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 231:
        remove_redis(idChat, idUser, chatData)
        aux = {}
        aux['search_term'] = msg
        requerido = get_content('/fs_scrapper/stores', [], aux)
        pretty_print(idChat, '/fs_scrapper/stores', requerido, True)
        return None

    elif menu == 232:
        remove_redis(idChat, idUser, chatData)
        if 'locationParam' in chatData:
            aux = {}
            aux['lat'] = float(chatData['locationParam']['lat'])
            aux['lon'] = float(chatData['locationParam']['lon'])
            requerido = get_content('/fs_scrapper/stores', [], aux)
            pretty_print(idChat, '/fs_scrapper/stores', requerido, True)
            return None
        else:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 241:
        if opcao == 1:
            save_redis(idChat, idUser, 242)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Pacotes com televisão','callback_data': '1'}],
                    [{'text': 'Telemóvel','callback_data': '2'}],
                    [{'text': 'Internet fixa','callback_data': '3'}],
                    [{'text': 'Internet móvel','callback_data': '4'}],
                    [{'text': 'Telefone','callback_data': '5'}],
                    [{'text': 'Ativação de pacotes Internet','callback_data': '6'}],
                    [{'text': 'Apoio informático','callback_data': '7'}],
                    [{'text': 'Sair','callback_data': '8'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 2:
            save_redis(idChat, idUser, 243)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Empresas','callback_data': '1'}],
                    [{'text': 'Corporate','callback_data': '2'}],
                    [{'text': 'Profissionais e empresas','callback_data': '3'}],
                    [{'text': 'Particulares','callback_data': '4'}],
                    [{'text': 'Sair','callback_data': '5'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            save_redis(idChat, idUser, 244)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Reparação de equipamentos','callback_data': '1'}],
                    [{'text': 'Devolução de equipamentos','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Denúncia de fraude / pirataria"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 5:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Contencioso"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 6:
            save_redis(idChat, idUser, 245)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Informações de portabilidade','callback_data': '1'}],
                    [{'text': 'Vídeo intérprete','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 7:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 242:
        if opcao == 1:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Pacotes com televisão"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 2:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Telemóvel"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Internet fixa"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Internet móvel"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 5:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Telefone"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 6:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Ativação pacotes internet"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 7:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Apoio informático"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 8:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 243:
        if opcao == 1:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Empresas"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 2:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Corporate"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] =  "Profissionais e empresas"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Particulares"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 5:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 244:
        if opcao == 1:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Reparação de equipamentos"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 2:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Devolução de equipamentos NOS"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 245:
        if opcao == 1:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "Video intérprete"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 2:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['assunto'] = "InfoPortabilidade"
            requerido = get_content('/fs_scrapper/linhas_apoio', [], aux)
            pretty_print(idChat, '/fs_scrapper/linhas_apoio', requerido, True)
            return None
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 251:
        if opcao == 1:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['nome'] = 'WTF 1GB'
            requerido = get_content('/fs_scrapper/wtf_name', [], aux)
            pretty_print(idChat, '/fs_scrapper/wtf_name', requerido, True)
            return None
        elif opcao == 2:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['nome'] = 'WTF 5GB'
            requerido = get_content('/fs_scrapper/wtf_name', [], aux)
            pretty_print(idChat, '/fs_scrapper/wtf_name', requerido, True)
            return None
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            aux = {}
            aux['nome'] = 'WTF 10GB'
            requerido = get_content('/fs_scrapper/wtf_name', [], aux)
            pretty_print(idChat, '/fs_scrapper/wtf_name', requerido, True)
            return None
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 261:
        remove_redis(idChat, idUser, chatData)
        aux = {}
        aux['name'] = msg
        requerido = get_content('/fs_scrapper/packages', [], aux)
        pretty_print(idChat, '/fs_scrapper/packages', requerido, True)
        return None

    elif menu == 262:
        if opcao == 1:
            save_string(idChat, idUser, '_package_type', 'fibra')
            save_redis(idChat, idUser, 263)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'TV','callback_data': '1'}],
                    [{'text': 'NET','callback_data': '2'}],
                    [{'text': 'TV+NET','callback_data': '3'}],
                    [{'text': 'TV+VOZ','callback_data': '4'}],
                    [{'text': 'TV+NET+VOZ','callback_data': '5'}],
                    [{'text': 'sair','callback_data': '6'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 2:
            save_string(idChat, idUser, '_package_type', 'satelite')
            save_redis(idChat, idUser, 263)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'TV','callback_data': '1'}],
                    [{'text': 'NET','callback_data': '2'}],
                    [{'text': 'TV+NET','callback_data': '3'}],
                    [{'text': 'TV+VOZ','callback_data': '4'}],
                    [{'text': 'TV+NET+VOZ','callback_data': '5'}],
                    [{'text': 'sair','callback_data': '6'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            save_redis(idChat, idUser, 263)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'TV','callback_data': '1'}],
                    [{'text': 'NET','callback_data': '2'}],
                    [{'text': 'TV+NET','callback_data': '3'}],
                    [{'text': 'TV+VOZ','callback_data': '4'}],
                    [{'text': 'TV+NET+VOZ','callback_data': '5'}],
                    [{'text': 'sair','callback_data': '6'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 263:
        if opcao == 1:
            save_string(idChat, idUser, '_package_service', 'TV')
            save_redis(idChat, idUser, 264)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'Qualquer preço','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 2:
            save_string(idChat, idUser, '_package_service', 'NET')
            save_redis(idChat, idUser, 264)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'Qualquer preço','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            save_string(idChat, idUser, '_package_service', 'TV+NET')
            save_redis(idChat, idUser, 264)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'Qualquer preço','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 4:
            save_string(idChat, idUser, '_package_service', 'TV+VOZ')
            save_redis(idChat, idUser, 264)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'Qualquer preço','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 5:
            save_string(idChat, idUser, '_package_service', 'TV+NET+VOZ')
            save_redis(idChat, idUser, 264)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'Qualquer preço','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 6:
            save_redis(idChat, idUser, 264)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'Qualquer preço','callback_data': '2'}],
                    [{'text': 'Sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 7:
            remove_string(idChat, idUser, '_package_type')
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 264:
        if opcao == 1:
            save_string(idChat, idUser, '_package_price', 'defined')
            save_redis(idChat, idUser, 265)
            data = {}
            data['msg'] = str('''Indique o valor mínimo que procura.''')
            return data
        elif opcao == 2:
            final_packages(idChat, idUser)
            remove_redis(idChat, idUser, chatData)
            return None
        elif opcao == 3:
            remove_string(idChat, idUser, '_package_type')
            remove_string(idChat, idUser, '_package_service')
            remove_redis(idChat, idUser, chatData)
            data = {}
            data['msg'] = str("Saiu do modo de regras.")
            return data

    elif menu == 265:
        valorMin = regexPrice(msg)
        save_float(idChat, idUser, '_min_value', valorMin)
        save_redis(idChat, idUser, 266)
        data = {}
        data['msg'] = str('''Indique o valor máximo que procura.''')
        return data

    elif menu == 266:
        valorMax = regexPrice(msg)
        save_float(idChat, idUser, '_max_value', valorMax)
        final_packages(idChat, idUser)
        remove_redis(idChat, idUser, chatData)
        return None
