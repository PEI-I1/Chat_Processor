import globals #redis_db
from utils import get_content, get_loc
from regex_rules_mode import regexPrice
import json


def load_redis(idChat, idUser):
    aux = globals.redis_db.get(str(idChat) + str(idUser) + '_rules_mode')

    if aux:
        return int(aux)
    else:
        return 0


def remove_redis(idChat, idUser, chatData):
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


def save_redis(idChat, idUser, menu):
    globals.redis_db.set(str(idChat) + str(idUser) + '_rules_mode', menu)


def save_number(idChat, idUser, code, number):
    globals.redis_db.set(str(idChat) + str(idUser) + code, number)


def load_number(idChat, idUser, code):
    aux = globals.redis_db.get(str(idChat) + str(idUser) + code)

    if aux:
        return int(aux)
    else:
        return None


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


def final_movies_options(idChat, idUser):
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

    return get_content('/scrapper/movies/search', [], aux)

def final_movies_duration(idChat, idUser):
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
        aux['date'] = duration
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

    return get_content('/scrapper/sessions/by_duration', [], aux)

def final_movies_duration_loc(idChat, idUser, chatData):
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    duration = load_string(idChat, idUser, '_movie_duration')
    date = load_string(idChat, idUser, '_movie_date')
    start = load_string(idChat, idUser, '_start_time')
    end = load_string(idChat, idUser, '_end_time')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    aux['lat'] = float(chatData['locationParam']['lat'])
    aux['lon'] = float(chatData['locationParam']['lon'])

    if duration:
        aux['date'] = duration
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

    return get_content('/scrapper/sessions/by_duration', [], aux)

def final_movies_loc(idChat, idUser, chatData):
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    aux['lat'] = float(chatData['locationParam']['lat'])
    aux['lon'] = float(chatData['locationParam']['lon'])

    return get_content('/scrapper/sessions/next_sessions', [], aux)

def final_movies_semloc(idChat, idUser):
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term') 

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    return get_content('/scrapper/sessions/next_sessions', [], aux)

def final_movies_sessoes_loc(idChat, idUser, chatData):
    aux = {}
    search_term = load_string(idChat, idUser, '_search_term')

    date = load_string(idChat, idUser, '_date')
    start = load_string(idChat, idUser, '_start_time')
    end = load_string(idChat, idUser, '_end_time')

    if search_term:
        aux['search_term'] = search_term
        remove_string(idChat, idUser, '_search_term')

    aux['lat'] = float(chatData['locationParam']['lat'])
    aux['lon'] = float(chatData['locationParam']['lon'])


    if date:
        aux['date'] = date
        remove_string(idChat, idUser, '_date')

    if start:
        aux['start_time'] = start
        remove_string(idChat, idUser, '_start_time')

    if end:
        aux['end_time'] = end
        remove_string(idChat, idUser, '_end_time')

    return get_content('/scrapper/sessions/by_date', [], aux)

def final_movies_sessoes(idChat, idUser):
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

    return get_content('/scrapper/sessions/by_date', [], aux)


def final_packages(idChat, idUser):
    aux =  {}
    tipo = load_string(idChat, idUser, '_package_type')
    servico = load_string(idChat, idUser, '_package_service')
    preco = load_string(idChat, idUser, '_package_price')

    if tipo:
        aux['type'] = tipo

    if servico:
        aux['service'] = servico

    if preco:
        aux['min'] = load_float(idChat, idUser, '_min_value')
        aux['max'] = load_float(idChat, idUser, '_max_value')

    return get_content('/fs_scrapper/packages', [], aux)


def final_phones(idChat, idUser):
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
    if brand:
        aux['brand'] = brand
    if promo:
        aux['promo'] = True
    if points:
        aux['points'] = True
    if prest:
        aux['prest'] = True
    if newPhones:
        aux['new'] = True
    if ofer:
        aux['ofer'] = True

    return get_content('/fs_scrapper/phones', [], aux)


def get_response_rules(idChat, idUser, msg, name, chatData):
    menu = load_redis(idChat, idUser)

    if menu == 0:
        save_redis(idChat, idUser, 1)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'cinemas ou sessões','callback_data': '1'}],
                [{'text': 'tarifários ou pacotes','callback_data': '2'}],
                [{'text': 'compra de telemóveis','callback_data': '3'}],
                [{'text': 'lojas da NOS','callback_data': '4'}],
                [{'text': 'linhas de apoio','callback_data': '5'}],
                [{'text': 'problemas técnicos','callback_data': '6'}],
                [{'text': 'sair','callback_data': '7'}]
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
            resposta = problem_rules(idChat, idUser, opcao, msg, chatData)
            return resposta

        elif opcao == 7:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

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
        reply_markup={
                'inline_keyboard': [
            [{'text': 'procurar cinemas','callback_data': '1'}],
            [{'text': 'filmes em sessão ','callback_data': '2'}],
            [{'text': 'filmes específicos','callback_data': '3'}],
            [{'text': 'próximas estreias','callback_data': '4'}],
            [{'text': 'informação de um filme','callback_data': '5'}],
            [{'text': 'sessões com certa duração','callback_data': '6'}],
            [{'text': 'proximas sessões','callback_data': '7'}],
            [{'text': 'sessões de um filme','callback_data': '8'}],
            [{'text': 'sessões por data','callback_data': '9'}],
            [{'text': 'sair','callback_data': '10'}]
        ]
    }
        data = {}
        data['msg'] = 'Escolha uma das seguintes opções.'
        data['menu'] = json.dumps(reply_markup)
        return data


    elif menu == 11:
        if opcao == 1:
            save_redis(idChat, idUser, 12)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'todos os cinemas','callback_data': '1'}],
                    [{'text': 'cinema em específico ','callback_data': '2'}],
                    [{'text': 'perto de localização','callback_data': '3'}],
                    [{'text': 'sair','callback_data': '4'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2:
            save_redis(idChat, idUser, 13)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'todos os cinemas','callback_data': '1'}],
                    [{'text': 'cinema em específico ','callback_data': '2'}],
                    [{'text': 'perto de localização','callback_data': '3'}],
                    [{'text': 'sair','callback_data': '4'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 3:
            save_redis(idChat, idUser, 14)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'genero','callback_data': '1'}],
                    [{'text': 'cast','callback_data': '2'}],
                    [{'text': 'produtor','callback_data': '3'}],
                    [{'text': 'sinopse','callback_data': '4'}],
                    [{'text': 'faixa etária','callback_data': '5'}],
                    [{'text': 'sair','callback_data': '6'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha o que pretende especificar.'
            data['menu'] = json.dumps(reply_markup)
            return data
            
        elif opcao == 4: # Apresentar próximas estreias
            requerido = get_content('/scrapper/movies/releases', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido

        elif opcao == 5:
            save_redis(idChat, idUser, 15)
            return str('''Especifique o filme que pretende obter infomações sobre.''')

        elif opcao == 6:
            save_redis(idChat, idUser, 16)
            return str('''Especifique a duração do filme que pretende, em minutos.''')

        elif opcao == 7:
            save_redis(idChat, idUser, 17)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 8:
            save_redis(idChat, idUser, 18)
            return str('''Especifique o nome do filme.''')

        elif opcao == 9:
            save_redis(idChat, idUser, 19)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 10:
            remove_redis(idChat, idUser, chatData)

    elif menu == 19:
        if opcao == 1:
            save_redis(idChat, idUser, 191)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'sim','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções'
            data['menu'] = json.dumps(reply_markup)
            return data
            
        if opcao == 2: # procurar sessoes por filme
            requerido = final_movies_sessoes(idChat, idUser)
            remove_redis(idChat, idUser, chatData)
            return requerido

    elif menu == 190:
        if opcao == 1:
            save_redis(idChat, idUser, 191)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'termo de pesquisa','callback_data': '1'}],
                    [{'text': 'localização','callback_data': '2'}],
                    [{'text': 'data (ano-mês-dia)','callback_data': '3'}],
                    [{'text': 'hora inicio das sessões','callback_data': '4'}],
                    [{'text': 'hora fim das sessões','callback_data': '5'}],
                    [{'text': 'sair','callback_data': '6'}],
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções para especificar'
            data['menu'] = json.dumps(reply_markup)
            return data
           
        if opcao == 2: # procurar sessoes por filme
            requerido = final_movies_sessoes_loc(idChat, idUser, chatData)
            remove_redis(idChat, idUser, chatData)
            return requerido

    elif menu == 191:
        if opcao == 1:
            save_redis(idChat, idUser, 199)
            return str('''Escreva termo de pesquisa para um cinema''')

        if opcao == 2: # procurar sessoes por filme
            save_redis(idChat, idUser, 198)
            return str('''Especifique a sua localização''')

        if opcao == 3: # procurar sessoes por filme
            save_redis(idChat, idUser, 197)
            return str('''Indique a data (ano-mês-dia)''')

        if opcao == 4: # procurar sessoes por filme
            save_redis(idChat, idUser, 196)
            return str('''Especifique limite para início das sessões''')

        if opcao == 5: # procurar sessoes por filme
            save_redis(idChat, idUser, 195)
            return str('''Especifique limite para fim das sessões''')

    elif menu == 199:
        save_string(idChat, idUser, '_search_term', msg)
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
                    [{'text': 'termo de pesquisa','callback_data': '1'}],
                    [{'text': 'localização','callback_data': '2'}],
                    [{'text': 'data (ano-mês-dia)','callback_data': '3'}],
                    [{'text': 'hora inicio das sessões','callback_data': '4'}],
                    [{'text': 'hora fim das sessões','callback_data': '5'}],
                    [{'text': 'sair','callback_data': '6'}],
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções para especificar'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: # procurar sessoes por filme
            requerido = final_movies_sessoes(idChat, idUser)
            #requerido = get_content('/scrapper/sessions/by_movie', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido

        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)

    elif menu == 181:
        if opcao == 1:
            save_redis(idChat, idUser, 189)
            return str('''Escreva termo de pesquisa para um cinema''')

        elif opcao == 2: # procurar sessoes por filme
            save_redis(idChat, idUser, 188)
            return str('''Especifique a sua localização''')

        elif opcao == 3: # procurar sessoes por filme
            save_redis(idChat, idUser, 187)
            return str('''Indique a data (ano-mês-dia)''')

        elif opcao == 4: # procurar sessoes por filme
            save_redis(idChat, idUser, 186)
            return str('''Especifique limite para início das sessões''')

        elif opcao == 5: # procurar sessoes por filme
            save_redis(idChat, idUser, 185)
            return str('''Especifique limite para fim das sessões''')

        elif opcao == 6:
            remove_redis(idChat, idUser, chatData)

    elif menu == 189:
        save_string(idChat, idUser, '_package_price', 'all')
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

    elif menu == 188:
        #save lat e lon
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
                    [{'text': 'termo de procura','callback_data': '1'}],
                    [{'text': 'usar localização','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Pretende especificar mais algum parametro?'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: # fazer a pesquisa sem localização
            requerido = final_movies_semloc(idChat, idUser)
            #requerido = get_content('/scrapper/sessions/next_sessions', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido

    elif menu == 108:
        if opcao == 1:
            save_redis(idChat, idUser, 169)
            return str('''Especifique termo de procura por cinema''')
        elif opcao == 2:
            save_redis(idChat, idUser, 168)
            return str('''Especifique localização''')
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)

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
                    [{'text': 'termo de pesquisa','callback_data': '1'},{'text': 'não','callback_data': '2'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções para especificar.'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: # fazer a pesquisa com localização
            requerido = final_movies_loc(idChat, idUser, chatData)
            #requerido = get_content('/scrapper/sessions/next_sessions', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido

    elif menu == 139:
        if opcao == 1:
            save_redis(idChat, idUser, 168)
            return str('''Especifique termo de procura por cinema''')
        elif opcao == 1:
            save_redis(idChat, idUser, 168)
            return str('''Especifique localização''')


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
                    [{'text': 'termo de pesquisa','callback_data': '1'}],
                    [{'text': 'localização','callback_data': '2'}],
                    [{'text': 'data (ano-mês-dia)','callback_data': '3'}],
                    [{'text': 'hora inicio das sessões','callback_data': '4'}],
                    [{'text': 'hora fim das sessões','callback_data': '5'}],
                    [{'text': 'sair','callback_data': '6'}],
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções para especificar'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: #fazer pesquisa de duração de filme
            #duracao = load_string(idChat, idUser, '_movie_duration')
            requerido = final_movies_duration(idChat, idUser)
            #requerido = get_content('/scrapper/sessions/by_duration', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido

    elif menu == 158:
        if opcao == 1:
            save_redis(idChat, idUser, 149)
            return str('''Escreva termo de pesquisa para um cinema''')

        elif opcao == 2: # procurar sessoes por filme
            save_redis(idChat, idUser, 148)
            return str('''Especifique a sua localização''')

        elif opcao == 3: # procurar sessoes por filme
            save_redis(idChat, idUser, 147)
            return str('''Indique a data (ano-mês-dia)''')

        elif opcao == 4: # procurar sessoes por filme
            save_redis(idChat, idUser, 146)
            return str('''Especifique limite para início das sessões''')

        elif opcao == 5: # procurar sessoes por filme
            save_redis(idChat, idUser, 145)
            return str('''Especifique limite para fim das sessões''')

        elif opcao == 6:
            remove_redis(idChat, idUser, chatData)

    elif menu == 149:
        save_string(idChat, idUser, '_package_price', 'all')
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

    elif menu == 148:
        #save lat e lon
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
                    [{'text': 'termo de pesquisa','callback_data': '1'}],
                    [{'text': 'localização','callback_data': '2'}],
                    [{'text': 'data (ano-mês-dia)','callback_data': '3'}],
                    [{'text': 'hora inicio das sessões','callback_data': '4'}],
                    [{'text': 'hora fim das sessões','callback_data': '5'}],
                    [{'text': 'sair','callback_data': '6'}],
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções para especificar'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: #fazer pesquisa de duração de filme
            #duracao = load_string(idChat, idUser, '_movie_duration')
            requerido = final_movies_duration_loc(idChat, idUser, chatData)
            #requerido = get_content('/scrapper/sessions/by_duration', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido

    elif menu == 15: # obter info do filme
        aux = {}
        aux['movie'] = msg
        requerido = get_content('/scrapper/movies/details', [], aux)
        remove_redis(idChat, idUser, chatData)
        return requerido

    elif menu == 14:
        if opcao == 1:
            save_redis(idChat, idUser, 179)
            return str('''Especifique que tipo de género pretende.''')

        elif opcao == 2:
            save_redis(idChat, idUser, 178)
            return str('''Especifique o cast, separando cada nome por vírgula.''')

        elif opcao == 3:
            save_redis(idChat, idUser, 177)
            return str('''Especifique um produtor.''')

        elif opcao == 4:
            save_redis(idChat, idUser, 176)
            return str('''Especifique expressões para procurar na sinopse''')

        elif opcao == 5:
            save_redis(idChat, idUser, 175)
            return str('''Especifique faixa etária''')

        elif opcao == 6:
            remove_redis(idChat, idUser, chatData)

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
                    [{'text': 'genero','callback_data': '1'}],
                    [{'text': 'cast','callback_data': '2'}],
                    [{'text': 'produtor','callback_data': '3'}],
                    [{'text': 'sinopse','callback_data': '4'}],
                    [{'text': 'faixa etária','callback_data': '5'}],
                    [{'text': 'sair','callback_data': '6'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha o que pretende especificar.'
            data['menu'] = json.dumps(reply_markup)
            return data

        elif opcao == 2: # fazer a pesquisa
            requerido = final_movies_options(idChat, idUser)
            #requerido = get_content('/scrapper/movies/search', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido

    elif menu == 13:
        if opcao == 1: #procurar cinemas sem dar nada
            requerido = get_content('/scrapper/movies/by_cinema', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
            
        elif opcao == 2: #procurar cinemas com query
            save_redis(idChat, idUser, 102)
            return str('''Insira uma expressão para procurar o cinema''')

        elif opcao == 3: #procurar cinemas com lat e long
            aux = {}
            aux['lat'] = float(chatData['locationParam']['lat'])
            aux['lon'] = float(chatData['locationParam']['lon'])
            requerido = get_content('/scrapper/movies/by_cinema', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido

        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)


    elif menu == 12:
        if opcao == 1: #procurar cinemas sem dar nada
            requerido = get_content('/scrapper/cinemas/search', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
            
        elif opcao == 2: #procurar cinemas com query
            save_redis(idChat, idUser, 101)
            return str('''Insira uma expressão para procurar o cinema''')

        elif opcao == 3: #procurar cinemas com lat e long
            aux = {}
            aux['lat'] = float(chatData['locationParam']['lat'])
            aux['lon'] = float(chatData['locationParam']['lon'])
            requerido = get_content('/scrapper/cinemas/search', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido

        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)

    elif menu == 101: #procurar cinemas com query
        aux = {}
        aux['search_term'] = msg
        requerido = get_content('/scrapper/cinemas/search', [], {})
        remove_redis(idChat, idUser, chatData)
        return requerido

    elif menu == 102: #procurar cinemas com query
        aux = {}
        aux['search_term'] = msg
        requerido = get_content('/scrapper/movies/by_cinema', [], aux)
        remove_redis(idChat, idUser, chatData)
        return requerido
        
def fs_rules(idChat, idUser, menu, msg, chatData):
    try:
        opcao = int(msg)
    except ValueError:
        opcao = -1

    if menu == 2:
        save_redis(idChat, idUser, 21)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'tarifários WTF','callback_data': '1'}],
                [{'text': 'pacotes','callback_data': '2'}],
                [{'text': 'sair','callback_data': '3'}]
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
                [{'text': 'modelo de telemóvel','callback_data': '1'}],
                [{'text': 'pesquisa sobre telemóveis','callback_data': '2'}],
                [{'text': 'top telemóveis mais vistos','callback_data': '3'}],
                [{'text': 'sair','callback_data': '4'}]
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
                [{'text': 'indicar zona prentendida','callback_data': '1'}],
                [{'text': 'lojas perto de si','callback_data': '2'}],
                [{'text': 'sair','callback_data': '3'}]
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
                [{'text': 'especificar assunto','callback_data': '1'}],
                [{'text': 'todas as linhas de apoio','callback_data': '2'}],
                [{'text': 'sair','callback_data': '3'}]
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
                    [{'text': 'todos os tarifários WTF','callback_data': '1'}],
                    [{'text': 'tarifários por nome','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
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
                    [{'text': 'indicar nome de pacote','callback_data': '1'}],
                    [{'text': 'pesquisa sobre pacotes','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das opções apresentadas.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

    elif menu == 22:
        if opcao == 1:
            save_redis(idChat, idUser, 221)
            return str("Indique o nome do modelo que pretende.")
        elif opcao == 2:
            save_redis(idChat, idUser, 222)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'especificar marca','callback_data': '1'}],
                    [{'text': 'modelos recentes','callback_data': '2'}],
                    [{'text': 'promoções','callback_data': '3'}],
                    [{'text': 'telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'pagamento a prestações','callback_data': '6'}],
                    [{'text': 'pagamento com pontos','callback_data': '7'}],
                    [{'text': 'apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            aux = {}
            aux['top'] = True
            requerido = get_content('/fs_scrapper/phones', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 4:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

    elif menu == 221:
        aux = {}
        aux['brand'] = msg
        requerido = get_content('/fs_scrapper/phones', [], aux)
        remove_redis(idChat, idUser, chatData)
        return requerido

    elif menu == 222:
        if opcao == 1:
           save_redis(idChat, idUser, 223)
           return str("Indique a marca que pretende")
        elif opcao == 2:
            save_string(idChat, idUser, '_new_phones_', 'defined')
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'especificar marca','callback_data': '1'}],
                    [{'text': 'modelos recentes','callback_data': '2'}],
                    [{'text': 'promoções','callback_data': '3'}],
                    [{'text': 'telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'pagamento a prestações','callback_data': '6'}],
                    [{'text': 'pagamento com pontos','callback_data': '7'}],
                    [{'text': 'apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'sair','callback_data': '9'}]
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
                    [{'text': 'especificar marca','callback_data': '1'}],
                    [{'text': 'modelos recentes','callback_data': '2'}],
                    [{'text': 'promoções','callback_data': '3'}],
                    [{'text': 'telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'pagamento a prestações','callback_data': '6'}],
                    [{'text': 'pagamento com pontos','callback_data': '7'}],
                    [{'text': 'apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'sair','callback_data': '9'}]
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
                    [{'text': 'especificar marca','callback_data': '1'}],
                    [{'text': 'modelos recentes','callback_data': '2'}],
                    [{'text': 'promoções','callback_data': '3'}],
                    [{'text': 'telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'pagamento a prestações','callback_data': '6'}],
                    [{'text': 'pagamento com pontos','callback_data': '7'}],
                    [{'text': 'apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 5:
            save_redis(idChat, idUser, 224)
            save_string(idChat, idUser, '_priceLimit_', 'defined')
            return str('''Indique o valor mínimo''')
        elif opcao == 6:
            save_string(idChat, idUser, '_prest_', 'defined')
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'especificar marca','callback_data': '1'}],
                    [{'text': 'modelos recentes','callback_data': '2'}],
                    [{'text': 'promoções','callback_data': '3'}],
                    [{'text': 'telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'pagamento a prestações','callback_data': '6'}],
                    [{'text': 'pagamento com pontos','callback_data': '7'}],
                    [{'text': 'apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'sair','callback_data': '9'}]
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
                    [{'text': 'especificar marca','callback_data': '1'}],
                    [{'text': 'modelos recentes','callback_data': '2'}],
                    [{'text': 'promoções','callback_data': '3'}],
                    [{'text': 'telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'pagamento a prestações','callback_data': '6'}],
                    [{'text': 'pagamento com pontos','callback_data': '7'}],
                    [{'text': 'apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 8:
            requerido = final_phones(idChat, idChat)
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
            return requerido
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
            return str("Saiu do modo de regras.")

    elif menu == 223:
        save_string(idChat, idUser, '_phones_brand_', msg)
        save_redis(idChat, idUser, 222)
        reply_markup={
            'inline_keyboard': [
                [{'text': 'especificar marca','callback_data': '1'}],
                [{'text': 'modelos recentes','callback_data': '2'}],
                [{'text': 'promoções','callback_data': '3'}],
                [{'text': 'telemóveis com ofertas','callback_data': '4'}],
                [{'text': 'definir intervalo de preços','callback_data': '5'}],
                [{'text': 'pagamento a prestações','callback_data': '6'}],
                [{'text': 'pagamento com pontos','callback_data': '7'}],
                [{'text': 'apresentar resultados da pesquisa','callback_data': '8'}],
                [{'text': 'sair','callback_data': '9'}]
            ]
        }
        data = {}
        data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
        data['menu'] = json.dumps(reply_markup)
        return data

    elif menu == 224:
        try:
            valorMin = regexPrice(msg)
            save_float(idChat, idUser, '_min_value_', valorMin)
            save_redis(idChat, idUser, 225)
            return str("Indique o valor máximo que procura.\n")
        except:
            return str("Por favor, volte a tentar inserindo o valor com dígitos e .")

    elif menu == 225:
        try:
            valorMax = regexPrice(msg)
            save_float(idChat, idUser, '_max_value_', valorMax)
            save_redis(idChat, idUser, 222)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'especificar marca','callback_data': '1'}],
                    [{'text': 'modelos recentes','callback_data': '2'}],
                    [{'text': 'promoções','callback_data': '3'}],
                    [{'text': 'telemóveis com ofertas','callback_data': '4'}],
                    [{'text': 'definir intervalo de preços','callback_data': '5'}],
                    [{'text': 'pagamento a prestações','callback_data': '6'}],
                    [{'text': 'pagamento com pontos','callback_data': '7'}],
                    [{'text': 'apresentar resultados da pesquisa','callback_data': '8'}],
                    [{'text': 'sair','callback_data': '9'}]
                ]
            }
            data = {}
            data['msg'] = 'Clique nas opções a que pretende restringir a pesquisa.'
            data['menu'] = json.dumps(reply_markup)
            return data
        except:
            return str("Por favor, volte a tentar inserindo o valor com dígitos e .")

    elif menu == 23:
        if opcao == 1:
            save_redis(idChat, idUser, 231)
            return str("Indique uma zona ou morada para a qual procura lojas NOS.")
        elif opcao == 2:
            save_redis(idChat, idUser, 232)
            get_loc(idChat)
            return str("Para prosseguir precisamos do seu consentimento, por favor prima o botão se concordar.")
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

    elif menu == 24:
        if opcao == 1:
            save_redis(idChat, idUser, 241)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'serviços NOS','callback_data': '1'}],
                    [{'text': 'entidades','callback_data': '2'}],
                    [{'text': 'equipamentos NOS','callback_data': '3'}],
                    [{'text': 'denúncia fraude/pirataria','callback_data': '4'}],
                    [{'text': 'faturas contencioso','callback_data': '5'}],
                    [{'text': 'informações','callback_data': '6'}],
                    [{'text': 'sair','callback_data': '7'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        if opcao == 2:
            requerido = get_content('/fs_scrapper/linhas_apoio', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

    elif menu == 25:
        if opcao == 1:
            requerido = get_content('/fs_scrapper/wtf', [], {})
            remove_redis(idChat, idUser, chatData)
            return requerido
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
            return str("Saiu do modo de regras.")

    elif menu == 26:
        if opcao == 1:
            save_redis(idChat, idUser, 261)
            return str('''Indique o nome do pacote pretendido.''')
        elif opcao == 2:
            save_redis(idChat, idUser, 262)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'pacotes fibra','callback_data': '1'}],
                    [{'text': 'pacotes satélite','callback_data': '2'}],
                    [{'text': 'todos os tipos de pacotes','callback_data': '3'}],
                    [{'text': 'sair','callback_data': '4'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 3:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

    elif menu == 231:
        aux = {}
        aux['search_term'] = msg
        requerido = get_content('/fs_scrapper/stores', [], aux)
        remove_redis(idChat, idUser, chatData)
        return requerido

    elif menu == 232:
        if 'locationParam' in chatData:
            aux = {}
            aux['lat'] = float(chatData['locationParam']['lat'])
            aux['lon'] = float(chatData['locationParam']['lon'])
            requerido = get_content('/fs_scrapper/stores', [], aux)
            remove_redis(idChat, idUser, chatData)
            return requerido
        else:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

    elif menu == 241:
        if opcao == 1:
            save_redis(idChat, idUser, 242)
            save_redis(idChat, idUser, 262)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'pacotes com televisão','callback_data': '1'}],
                    [{'text': 'telemóvel','callback_data': '2'}],
                    [{'text': 'Internet fixa','callback_data': '3'}],
                    [{'text': 'Internet móvel','callback_data': '4'}],
                    [{'text': 'telefone','callback_data': '5'}],
                    [{'text': 'ativação de pacotes Internet','callback_data': '6'}],
                    [{'text': 'apoio informático','callback_data': '7'}],
                    [{'text': 'sair','callback_data': '8'}]
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
                    [{'text': 'empresas','callback_data': '1'}],
                    [{'text': 'corporate','callback_data': '2'}],
                    [{'text': 'profissionais e empresas','callback_data': '3'}],
                    [{'text': 'particulares','callback_data': '4'}],
                    [{'text': 'sair','callback_data': '5'}]
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
                    [{'text': 'reparação de equipamentos','callback_data': '1'}],
                    [{'text': 'devolução de equipamentos','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
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
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'informações de portabilidade','callback_data': '1'}],
                    [{'text': 'vídeo intérprete','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 7:
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

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
            return str("Saiu do modo de regras.")

    elif menu == 263:
        if opcao == 1:
            save_string(idChat, idUser, '_package_service', 'TV')
            save_redis(idChat, idUser, 264)
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'qualquer preço','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
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
                    [{'text': 'definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'qualquer preço','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
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
                    [{'text': 'definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'qualquer preço','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
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
                    [{'text': 'definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'qualquer preço','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
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
                    [{'text': 'definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'qualquer preço','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
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
                    [{'text': 'definir intervalo de preços','callback_data': '1'}],
                    [{'text': 'qualquer preço','callback_data': '2'}],
                    [{'text': 'sair','callback_data': '3'}]
                ]
            }
            data = {}
            data['msg'] = 'Escolha uma das seguintes opções.'
            data['menu'] = json.dumps(reply_markup)
            return data
        elif opcao == 7:
            remove_string(idChat, idUser, '_package_type')
            remove_redis(idChat, idUser, chatData)
            return str("Saiu do modo de regras.")

    elif menu == 264:
        if opcao == 1:
            save_string(idChat, idUser, '_package_price', 'defined')
            save_redis(idChat, idUser, 265)
            return str("Indique o valor mínimo que procura.")
        elif opcao == 2:
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
    chatData["status"] == "modo problemas"
    return str("Vamos tentar encontrar uma solução para o seu problema.")
