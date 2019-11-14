TRAIN_DATA = [
    # DATE datas

    # MOVIE nomes de filmes
    ("Quando dá o filme Joker?", {"entities": [(18, 23, "MOVIE")]}),
    ("Quero ver o filme Guerra dos Mundos amanhã.", {"entities": [(18, 24, "MOVIE"), (25, 28, "MOVIE"), (29, 35, "MOVIE"), (36, 42, "DATE")]}),
    ("Quero ver o filme Guerra dos Mundos amanhã.", {"entities": [(18, 35, "MOVIE"), (36, 42, "DATE")]}),
    ("Quando começa o filme A Herdade?", {"entities": [(22, 31, "MOVIE")]}),
    ("Qual a duração do filme Doutor Sono?", {"entities": [(24, 35, "MOVIE")]}),
    # LOC Local por coordenadas (latitude e longitude)
    ("Que filmes tens em Braga?", {"entities": [(19, 24, "LOC")]}),
    ("Que filmes tens no Porto?", {"entities": [(19, 24, "LOC")]}),
    # DURATION duração de algo
    ("Filmes com menos de 1h", {"entities": [(20, 22, "DURATION")]}),
    ("Filmes com menos de uma hora", {"entities": [(20, 28, "DURATION")]}),
    ("Filmes com mais de 1h", {"entities": [(19, 21, "DURATION")]}),
    ("Filmes com mais de uma hora", {"entities": [(19, 27, "DURATION")]}),
    ("Filmes com menos de 1 hora", {"entities": [(20, 26, "DURATION")]}),
    ("Filmes com menos de 1h30min", {"entities": [(20, 27, "DURATION")]}),
    ("Filmes com menos de 1:30min", {"entities": [(20, 27, "DURATION")]}),
    ("Filmes com menos de 1 hora e 30 minutos", {"entities": [(20, 39, "DURATION")]}),
    # GENRE genero do filme
    ("Quero ver filmes de terror", {"entities": [(20, 26, "GENRE")]}),
    ("Quero ver filmes de comédia", {"entities": [(20, 27, "GENRE")]}),
    ("Que filmes há de ação?", {"entities": [(17, 21, "GENRE")]}),
    ("Que filmes há de animação?", {"entities": [(17, 25, "GENRE")]}),
    # PER nomes, pessoas (atores, realizadores)
    ("Que filmes há com o Will Smith?", {"entities": [(20, 30, "PER")]}),
    ("Filmes com o Will Smith", {"entities": [(13, 23, "PER")]}),
    # AGERESTRIC restriçao de idade
    ("Que filmes há para crianças?", {"entities": [(19, 27, "AGERESTRIC")]}),
    ("Que filmes há para adultos?", {"entities": [(19, 26, "AGERESTRIC")]}),
    ("Que filmes há para 18+?", {"entities": [(19, 22, "AGERESTRIC")]}),
    ("Que filmes há para 18-?", {"entities": [(19, 22, "AGERESTRIC")]}),
    ("Que filmes há para mais de 18anos?", {"entities": [(27, 33, "AGERESTRIC")]}),
    ("Que filmes há para menos de 18anos?", {"entities": [(28, 34, "AGERESTRIC")]}),

    # MODEL modelo de telemovel
    ("Quero informações sobre o iPhone 8", {"entities": [(26, 34, "MODEL")]}),
    ("Quero informações sobre o iPhone 11", {"entities": [(26, 35, "MODEL")]}),
    ("Quero informações sobre o Asus Zenfone", {"entities": [(26, 38, "MODEL")]}),
    # BRAND marcas de telemovel
    ("Quero telemoveis da Apple", {"entities": [(20, 25, "BRAND")]}),
    ("Que telemoveis da Apple estão disponiveis?", {"entities": [(18, 23, "BRAND")]}),
    ("Telemoveis da Apple", {"entities": [(14, 19, "BRAND")]}),
    ("Quero telemoveis da Asus", {"entities": [(20, 24, "BRAND")]}),
    ("Quero telemoveis da Xiaomi", {"entities": [(20, 26, "BRAND")]}),
    # MONEY Valores monetários
    ("Telemoveis abaixo dos 100euros", {"entities": [(22, 30, "MONEY")]}),
    ("Telemoveis acima dos 100euros", {"entities": [(21, 29, "MONEY")]}),
    ("Telemoveis abaixo dos 70euros", {"entities": [(22, 29, "MONEY")]}),
    ("Telemoveis abaixo dos 70euros e 50 centimos", {"entities": [(22, 43, "MONEY")]}),
    ("Telemoveis abaixo dos 70€", {"entities": [(22, 25, "MONEY")]}),
    ("Telemoveis abaixo dos 70,50€", {"entities": [(22, 28, "MONEY")]}),
    ("Tens algum telemovel abaixo dos 70€?", {"entities": [(28, 31, "MONEY")]}),
    # PACKAGE     Pacotes
    # SPEED       Velocidade da net
]

### entidades uteis ###
# Datas
## problemas tecnicos
## filmes
# MOVIE       Filmes
# LOC         Local por coordenadas (latitude e longitude)
# DURATION    Duração (tempo)
# GENRE       Géneros de filmes
# PER         Nomes de pessoas (atores, realizadores)
# AGERESTRIC  restriçao de idade
## assistencia
#       Assunto (linha apoio)
## telemoveis
# MODEL       Modelos de telemóveis
# BRAND       Marcas de telemóveis
# MONEY       Valores monetários
# PACKAGE     Pacotes
# SPEED       Velocidade da net
#       Tarifários
#       Locais (Lojas NOS)
