# example, on some cinemas end-points 'lat' and 'lon' are required or 'search_term'
cat = [
    {
        'request': '/fs_scrapper/linhas_apoio',
        'service': 'FS_SCRAPER',
        'words': ['linhas','linha','apoio','assunto','numero','contacto','contactos','empresa','empresas','aderir','informacoes','adicionais','informacao','adicional','servicos','chamada','chamadas','ligar','falar',"assistente"],
        'paramsRequired': {},
        'paramsOptional': {'0': 'SUBJECT'},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/fs_scrapper/phone_model',
        'service': 'FS_SCRAPER',
        'words': ['modelos','modelo','telemovel','telemoveis'],
        'paramsRequired': {'0':'PRODUCT'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : 'Por favor, diga-nos o modelo de telemóvel que procura.'
    },
    {
        'request': '/fs_scrapper/brand_phones',
        'service': 'FS_SCRAPER',
        'words': ['marca','marcas','comprar','telemovel','telemoveis','preco'],
        'paramsRequired': {'0':'ORG'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : 'Por favor, diga-nos a marca de telemóveis que procura.'
    },
    {
        'request': '/fs_scrapper/top_phones',
        'service': 'FS_SCRAPER',
        'words': ['top','telemovel','telemoveis','melhores','link'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/fs_scrapper/promo_phones',
        'service': 'FS_SCRAPER',
        'words': ['promocoes','promocao','desconto','descontos','barato','baratos','telemovel','telemoveis'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/fs_scrapper/new_phones',
        'service': 'FS_SCRAPER',
        'words': ['novidades','novos','telemovel','telemoveis','recente','recentes'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/fs_scrapper/ofer_phones',
        'service': 'FS_SCRAPER',
        'words': ['oferta','telemovel','telemoveis', 'extra'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/fs_scrapper/prest_phones',
        'service': 'FS_SCRAPER',
        'words': ['prestacoes','prestacao','telemovel','telemoveis'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/fs_scrapper/points_phones',
        'service': 'FS_SCRAPER',
        'words': ['ponto','pontos','telemovel','telemoveis'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/fs_scrapper/phones_price',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preco','telemovel','telemoveis'],
        'paramsRequired': {'0':'MONEY', '1':'MONEY'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : 'Por favor, forneça um valor mínimo e um valor máximo.'
    },

    #TODO falta aqui 4 routes   -- preciso de saber primeiro se tenho que mudar a api

    {
        'request': '/fs_scrapper/all_wtf',
        'service': 'FS_SCRAPER',
        'words': ['tarifarios','telemovel','wtf'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''

    },
    {
        'request': '/fs_scrapper/wtf_name',
        'service': 'FS_SCRAPER',
        'words': ['tarifario','telemovel','wtf'],
        'paramsRequired': {'0':'NAME'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : 'Por favor, diga-nos o nome do tarifário WTF que pretende.'

    },
    {
        'request': '/fs_scrapper/stores_zone',
        'service': 'FS_SCRAPER',
        'words': ['loja','lojas','zona'],
        'paramsRequired': {'0':'GPE'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : 'Por favor, diga-nos a zona do país que procura.'
    },
    {
        'request': '/fs_scrapper/store_address',
        'service': 'FS_SCRAPER',
        'words': ['morada','loja','lojas'],
        'paramsRequired': {'0':'FAC'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : 'Por favor, diga-nos a morada da loja que procura.'
    },
    #TODO falta o specific package   -- preciso de saber primeiro se tenho que mudar a api
    {
        'request': '/fs_scrapper/packages',
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
        'request': '/fs_scrapper/fiber_packages',
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
        'request': '/fs_scrapper/satelite_packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes', 'satelite', 'satelite'],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/fs_scrapper/packages_service',
        'service': 'FS_SCRAPER',
        'words': ['pacote','pacotes', 'servicos', 'servico', 'TV', 'NET', 'TV+NET', 'TV+VOZ', 'TV+NET+VOZ'],
        'paramsRequired': {'0':'PACKAGE'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    },
    {
        'request': '/fs_scrapper/packages_price',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preco','pacote','pacotes'],
        'paramsRequired': {'0':'MONEY', '1':'MONEY'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : 'Por favor, forneça um valor mínimo e um valor máximo.'
    },
    #TODO faltam os últimos 5 métodos   -- preciso de saber primeiro se tenho que mudar a api
    # CINEMAS
    {
        'request': '/scrapper/cinemas/search',
        'service': 'CINEMA_SCRAPER',
        'words': ['cinema', 'perto', 'proximo', 'estou', 'aqui', 'localidade', 'cidade', 'sitio', 'distrito', 'concelho', 'morada'],
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
        'words': ['cinema', 'perto', 'proximo', 'estou', 'aqui', 'localidade', 'cidade', 'sitio', 'distrito', 'concelho', 'morada', 'filme', 'filmes'],
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
        'words': ['filme', 'pelicula', 'video', 'procura', 'consulta', 'sobre'],
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
        'words': {'filme', 'pelicula', 'video', 'estreias', 'estreia', 'novo', 'estrear', 'lancamento'},
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
        'words': ['filme', 'pelicula', 'video', 'detalhes', 'informacao', 'informacoes', 'sobre', 'casting', 'ator', 'produtor', 'realizador', 'tipo', 'genero', 'categoria', 'sinopse', 'historia', 'idade', 'restricao', 'criancas', 'adultos'],
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
        'words': ['sessao', 'sessoes', 'exibicao', 'exibicoes', 'duracao', 'tempo', 'tamanho', 'demora', 'extensao', 'minutos', 'horas', 'hora'],
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
        'words': ['sessao', 'sessoes', 'exibicao', 'exibicoes', 'seguir', 'proximas', 'agora', 'seguintes', 'prestes'],
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
        'words': ['sessao', 'sessoes', 'exibicao', 'exibicoes', 'proximas', 'filme'],
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
        'words': ['sessao', 'sessoes', 'exibicao', 'exibicoes', 'proximas', 'dia', 'horas', 'hora', 'inicio', 'fim', 'hoje', 'amanhã', 'segunda', 'segunda-feira', 'terca', 'terca-feira', 'quarta', 'quarta-feira', 'quinta', 'quinta-feira', 'sexta', 'sexta-feira', 'sabado', 'domingo'],
        'paramsRequired': {},
        'paramsOptional': {'date':'DATE', 'start_time':'TIME', 'end_time':'TIME'},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False,
        'missingRequiredParamsPhrase' : ''
    }
]
