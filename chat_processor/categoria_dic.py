# TODO, support more parameters combination
# example, on some cinemas end-points 'lat' and 'lon' are required or 'search_term'
cat = [
    {
        'request': 'linhas_apoio',
        'service': 'FS_SCRAPER',
        'words': ['linhas','linha','apoio','assunto','número','contacto','contactos','empresa','empresas','aderir','informações','adicionais','informação','adicional','serviços','chamada','chamadas','ligar','falar',"assistente"],
        'params': ['SUBJECT'],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'phone_model',
        'service': 'FS_SCRAPER',
        'words': ['modelos','modelo','telemóvel','telemóveis'],
        'params': ['PRODUCT'],
        'paramsOpcional': [],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': False
    },
    {
        'request': 'brand_phones',
        'service': 'FS_SCRAPER',
        'words': ['marca','marcas','comprar','telemóvel','telemóveis','preço'],
        'params': ['ORG'],
        'paramsOpcional': [],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': False
    },
    {
        'request': 'top_phones',
        'service': 'FS_SCRAPER',
        'words': ['top','telemóvel','telemóveis','melhores','link'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'promo_phones',
        'service': 'FS_SCRAPER',
        'words': ['promoções','promoção','desconto','descontos','barato','baratos','telemóvel','telemóveis'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'new_phones',
        'service': 'FS_SCRAPER',
        'words': ['novidades','novos','telemóvel','telemóveis','recente','recentes'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'ofer_phones',
        'service': 'FS_SCRAPER',
        'words': ['oferta','telemóvel','telemóveis'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'prest_phones',
        'service': 'FS_SCRAPER',
        'words': ['prestações','prestação','telemóvel','telemóveis'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'points_phones',
        'service': 'FS_SCRAPER',
        'words': ['ponto','pontos','telemóvel','telemóveis'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'phones_by_price',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preço','telemóvel','telemóveis'],
        'params': ['MONEY', 'MONEY'],
        'paramsOpcional': [],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': False
    },
    {
        'request': 'all_wtf',
        'service': 'FS_SCRAPER',
        'words': ['tarifários','telemóvel','wtf'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'stores_by_zone',
        'service': 'FS_SCRAPER',
        'words': ['loja','lojas','zona'],
        'params': ['GPE'],
        'paramsOpcional': [],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': False
    },
    {
        'request': 'store_address',
        'service': 'FS_SCRAPER',
        'words': ['morada','loja','lojas'],
        'params': ['FAC'],
        'paramsOpcional': [],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': False
    },
    {
        'request': 'packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'fiber_packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes', 'fibra'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'satelite_packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes', 'satelite', 'satélite'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': 'packages_service',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preço','pacote','pacotes'],
        'params': ['PACKAGE'],
        'paramsOpcional': [],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': False
    },
    {
        'request': 'packages_price',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preço','pacote','pacotes'],
        'params': ['MONEY', 'MONEY'],
        'paramsOpcional': [],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': False
    },
    # CINEMAS
    {
        'request': '/scrapper/cinemas/search',
        'service': 'CINEMA_SCRAPER',
        'words': ['cinema', 'perto', 'próximo', 'estou', 'aqui', 'localidade', 'cidade', 'sítio', 'distrito', 'concelho', 'morada'],
        'params': ['search_term', 'lat', 'lon'],
        'paramsOpcional': ['search_term', 'lat', 'lon'],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': True
    },
    {
        'request': '/scrapper/movies/by_cinema',
        'service': 'CINEMA_SCRAPER',
        'words': ['cinema', 'perto', 'próximo', 'estou', 'aqui', 'localidade', 'cidade', 'sítio', 'distrito', 'concelho', 'morada', 'filme', 'filmes'],
        'params': ['search_term', 'lat', 'lon'],
        'paramsOpcional': ['search_term', 'lat', 'lon'],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': True
    },
    {
        'request': '/scrapper/movies/search',
        'service': 'CINEMA_SCRAPER',
        'words': ['filme', 'película', 'vídeo', 'procura', 'consulta', 'sobre'],
        'params': ['genre', 'cast', 'producer', 'synopsis', 'age'],
        'paramsOpcional': ['genre', 'cast', 'producer', 'synopsis', 'age'],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': True
    },
    {
        'request': '/scrapper/movies/releases',
        'service': 'CINEMA_SCRAPER',
        'words': ['filme', 'película', 'vídeo', 'estreias', 'estreia', 'novo', 'estrear', 'lançamento'],
        'params': [],
        'paramsOpcional': [],
        'canRequestWithoutParams': True,
        'needAtLeastOneParam': False
    },
    {
        'request': '/scrapper/movies/details',
        'service': 'CINEMA_SCRAPER',
        'words': ['filme', 'película', 'vídeo', 'detalhes', 'informação', 'informações', 'sobre', 'casting', 'ator', 'produtor', 'realizador', 'tipo', 'género', 'categoria', 'sinopse', 'história', 'idade', 'restrição', 'crianças', 'adultos'],
        'params': ['movie'],
        'paramsOpcional': [],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': True
    },
    {
        'request': '/scrapper/sessions/by_duration',
        'service': 'CINEMA_SCRAPER',
        'words': ['sessão', 'sessões', 'exibição', 'exibições', 'duração', 'tempo', 'tamanho', 'demora', 'extensão', 'minutos', 'horas', 'hora'],
        'params': ['search_term', 'lat', 'lon', 'duration', 'date', 'time'],
        'paramsOpcional': ['search_term', 'lat', 'lon', 'date', 'time'],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': True
    },
    {
        'request': '/scrapper/sessions/next_sessions',
        'service': 'CINEMA_SCRAPER',
        'words': ['sessão', 'sessões', 'exibição', 'exibições', 'seguir', 'próximas', 'agora', 'seguintes', 'prestes'],
        'params': ['search_term', 'lat', 'lon'],
        'paramsOpcional': ['search_term', 'lat', 'lon'],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': True
    },
    {
        'request': '/scrapper/sessions/by_movie',
        'service': 'CINEMA_SCRAPER',
        'words': ['sessão', 'sessões', 'exibição', 'exibições', 'próximas', 'filme'],
        'params': ['search_term', 'lat', 'lon', 'movie', 'date', 'time'],
        'paramsOpcional': ['search_term', 'lat', 'lon', 'date', 'time'],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': True
    },
    {
        'request': '/scrapper/sessions/by_date',
        'service': 'CINEMA_SCRAPER',
        'words': ['sessão', 'sessões', 'exibição', 'exibições', 'próximas', 'dia', 'horas', 'hora', 'início', 'fim', 'hoje', 'amanhã', 'segunda', 'segunda-feira', 'terça', 'terça-feira', 'quarta', 'quarta-feira', 'quinta', 'quinta-feira', 'sexta', 'sexta-feira', 'sábado', 'domingo'],
        'params': ['search_term', 'lat', 'lon', 'date', 'start_time', 'end_time'],
        'paramsOpcional': ['search_term', 'lat', 'lon', 'date', 'start_time', 'end_time'],
        'canRequestWithoutParams': False,
        'needAtLeastOneParam': True
    }
]