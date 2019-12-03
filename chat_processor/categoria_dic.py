# TODO, comfirmar os pedidos do FS_scrapper
# example, on some cinemas end-points 'lat' and 'lon' are required or 'search_term'
cat = [
    {
        'request': 'fs_scrapper/linhas_apoio',
        'service': 'FS_SCRAPER',
        'words': ['linhas','linha','apoio','assunto','número','contacto','contactos','empresa','empresas','aderir','informações','adicionais','informação','adicional','serviços','chamada','chamadas','ligar','falar',"assistente"],
        'paramsRequired': {},
        'paramsOptional': {'0': 'SUBJECT'},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : 'Por favor, diga-nos o assunto em que precisa de apoio.'
    },
    {
        'request': 'fs_scrapper/phone_model',
        'service': 'FS_SCRAPER',
        'words': ['modelos','modelo','telemóvel','telemóveis'],
        'paramsRequired': {'0':'PRODUCT'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/brand_phones',
        'service': 'FS_SCRAPER',
        'words': ['marca','marcas','comprar','telemóvel','telemóveis','preço'],
        'paramsRequired': {'0':'ORG'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/top_phones',
        'service': 'FS_SCRAPER',
        'words': ['top','telemóvel','telemóveis','melhores','link'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/promo_phones',
        'service': 'FS_SCRAPER',
        'words': ['promoções','promoção','desconto','descontos','barato','baratos','telemóvel','telemóveis'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/new_phones',
        'service': 'FS_SCRAPER',
        'words': ['novidades','novos','telemóvel','telemóveis','recente','recentes'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/ofer_phones',
        'service': 'FS_SCRAPER',
        'words': ['oferta','telemóvel','telemóveis'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/prest_phones',
        'service': 'FS_SCRAPER',
        'words': ['prestações','prestação','telemóvel','telemóveis'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/points_phones',
        'service': 'FS_SCRAPER',
        'words': ['ponto','pontos','telemóvel','telemóveis'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/phones_price',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preço','telemóvel','telemóveis'],
        'paramsRequired': {'0':'MONEY', '1':'MONEY'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : 'Por favor, forneça um valor mínimo e um valor máximo.'
    },
    {
        'request': 'fs_scrapper/all_wtf',
        'service': 'FS_SCRAPER',
        'words': ['tarifários','telemóvel','wtf'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''

    },
    {
        'request': 'fs_scrapper/stores_zone',
        'service': 'FS_SCRAPER',
        'words': ['loja','lojas','zona'],
        'paramsRequired': {'0':'GPE'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/store_address',
        'service': 'FS_SCRAPER',
        'words': ['morada','loja','lojas'],
        'paramsRequired': {'0':'FAC'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/fiber_packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes', 'fibra'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/satelite_packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes', 'satelite', 'satélite'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/packages_service',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preço','pacote','pacotes'],
        'paramsRequired': {'0':'PACKAGE'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': 'fs_scrapper/packages_price',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preço','pacote','pacotes'],
        'paramsRequired': {'0':'MONEY', '1':'MONEY'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    # CINEMAS
    {
        'request': '/scrapper/cinemas/search',
        'service': 'CINEMA_SCRAPER',
        'words': ['cinema', 'perto', 'próximo', 'estou', 'aqui', 'localidade', 'cidade', 'sítio', 'distrito', 'concelho', 'morada'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/scrapper/movies/by_cinema',
        'service': 'CINEMA_SCRAPER',
        'words': ['cinema', 'perto', 'próximo', 'estou', 'aqui', 'localidade', 'cidade', 'sítio', 'distrito', 'concelho', 'morada', 'filme', 'filmes'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/scrapper/movies/search',
        'service': 'CINEMA_SCRAPER',
        'words': ['filme', 'película', 'vídeo', 'procura', 'consulta', 'sobre'],
        'paramsRequired': {},
        'paramsOptional': {'genre':'', 'cast':'PERSON', 'producer':'PERSON', 'synopsis':'', 'age':'CARDINAL'},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': True,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/scrapper/movies/releases',
        'service': 'CINEMA_SCRAPER',
        'words': {'filme', 'película', 'vídeo', 'estreias', 'estreia', 'novo', 'estrear', 'lançamento'},
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/scrapper/movies/details',
        'service': 'CINEMA_SCRAPER',
        'words': ['filme', 'película', 'vídeo', 'detalhes', 'informação', 'informações', 'sobre', 'casting', 'ator', 'produtor', 'realizador', 'tipo', 'género', 'categoria', 'sinopse', 'história', 'idade', 'restrição', 'crianças', 'adultos'],
        'paramsRequired': {'0':'WORK OF ART'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/scrapper/sessions/by_duration',
        'service': 'CINEMA_SCRAPER',
        'words': ['sessão', 'sessões', 'exibição', 'exibições', 'duração', 'tempo', 'tamanho', 'demora', 'extensão', 'minutos', 'horas', 'hora'],
        'paramsRequired': {'0':'TIME'},
        'paramsOptional': {'date':'DATE', 'time':'TIME'},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/scrapper/sessions/next_sessions',
        'service': 'CINEMA_SCRAPER',
        'words': ['sessão', 'sessões', 'exibição', 'exibições', 'seguir', 'próximas', 'agora', 'seguintes', 'prestes'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/scrapper/sessions/by_movie',
        'service': 'CINEMA_SCRAPER',
        'words': ['sessão', 'sessões', 'exibição', 'exibições', 'próximas', 'filme'],
        'paramsRequired': {'0':'WORK OF ART'},
        'paramsOptional': {'date':'DATE', 'time':'TIME'},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/scrapper/sessions/by_date',
        'service': 'CINEMA_SCRAPER',
        'words': ['sessão', 'sessões', 'exibição', 'exibições', 'próximas', 'dia', 'horas', 'hora', 'início', 'fim', 'hoje', 'amanhã', 'segunda', 'segunda-feira', 'terça', 'terça-feira', 'quarta', 'quarta-feira', 'quinta', 'quinta-feira', 'sexta', 'sexta-feira', 'sábado', 'domingo'],
        'paramsRequired': {},
        'paramsOptional': {'date':'DATE', 'start_time':'TIME', 'end_time':'TIME'},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    }
]
