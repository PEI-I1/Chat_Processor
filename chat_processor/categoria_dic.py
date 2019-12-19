cat = [
    # FS
    {
        'request': '/fs_scrapper/linhas_apoio',
        'service': 'FS_SCRAPER',
        'words': [(r'linhas?', 1.0), (r'apoio', 1.0), (r'assunto', 1.0),(r'numero', 1.0), (r'contactos?', 1.0), (r'empresas?', 1.0), (r'aderir', 1.0), (r'informac(ao|oes)', 1.0), (r'servicos', 1.0), (r'chamadas?', 1.0), (r'assistente', 1.0), (r'linhas? de apoio', 2.0)],
        'paramsRequired': {},
        'paramsOptional': {'assunto': 'SUBJECT'},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/fs_scrapper/phones',
        'service': 'FS_SCRAPER',
        'words': [(r'modelos?', 1.0), (r'marcas?', 1.0), (r'telemove(l|is)', 1.0), (r'telemove(l|is).+marcas?', 2.0), (r'top', 1.0), (r'promo(cao|coes)?', 1.5), (r'descontos?', 1.0), (r'telemove(l|is).+promo(cao|coes)?', 2.0), (r'novidades?', 1.0),(r'novos?', 1.0), (r'telemove(l|is).+novos?', 2.0), (r'telemove(l|is).+recentes?', 2.0), (r'(com )?ofertas?', 1.0), (r'extra', 1.0), (r'pagamentos? a prestac(ao|oes)', 2.0), (r'prestac(ao|oes)', 1.0), (r'pontos?', 1.0), (r'preco', 1.0), (r'preco maximo', 1.0), (r'preco minimo', 1.0), (r'preco entre', 2.0)],
        'paramsRequired': {},
        'paramsOptional': {'top':'PHONES_BOOLEAN', 'new':'PHONES_BOOLEAN', 'promo':'PHONES_BOOLEAN', 'ofer':'PHONES_BOOLEAN', 'prest':'PHONES_BOOLEAN', 'points':'PHONES_BOOLEAN', 'brand':'ORG|PRODUCT', 'min':'MONEY', 'max':'MONEY'},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/fs_scrapper/wtf',
        'service': 'FS_SCRAPER',
        'words': [(r'tarifarios?', 1.0), (r'todos', 1.0), (r'telemovel', 1.0), (r'wtf', 1.0), (r'todos (os )?tarifarios', 2.0)],
        'paramsRequired': {},
        'paramsOptional': {'nome':'TARIFF'},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False

    },
    {
        'request': '/fs_scrapper/stores',
        'service': 'FS_SCRAPER',
        'words': [(r'lojas?', 1.0),(r'zona', 1.0),(r'onde', 1.0),(r'est(a|ao)', 1.0), (r'morada', 1.0), (r'rua', 1.0), (r'lojas?.+rua', 1.5), (r'lojas?.+morada', 1.5)],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {'search_term':'GPE|FAC', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/fs_scrapper/packages',
        'service': 'FS_SCRAPER',
        'words': [(r'pacotes?', 1.0), (r'fibra', 1.0), (r'pacotes.+fibra', 1.0), (r'satelite', 1.0), (r'pacotes.+satelite', 1.0), (r'servicos?', 1.0),(r'TV', 1.0), (r'NET', 1.0), (r'TV+NET', 1.0), (r'TV+VOZ', 1.0), (r'preco', 1.0)],
        'paramsRequired': {},
        'paramsOptional': {'type':'PACKAGE_TYPE', 'name':'PACKAGE', 'service':'PACKAGE_SERVICE', 'min':'MONEY', 'max':'MONEY'},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False
    },
    # CINEMAS
    {
        'request': '/scrapper/cinemas/search',
        'service': 'CINEMA_SCRAPER',
        'words': [(r'cinema', 1.0), (r'perto', 1.0), (r'proximos?', 1.0), (r'aqui', 1.0), (r'localidade', 1.0), (r'cidade', 1.0),
                  (r'sitio', 1.0), (r'distrito', 1.0), (r'concelho', 1.0), (r'morada', 1.0), (r'cinemas?.+perto', 2.0),
                  (r'cinemas?.+aqui', 1.0), (r'cinemas?.+proximos?', 1.0)],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/scrapper/movies/by_cinema',
        'service': 'CINEMA_SCRAPER',
        'words': [(r'cinemas?', 1.0), (r'perto', 1.0), (r'proximo', 1.0), (r'estou', 1.0), (r'aqui', 1.0), (r'localidade', 1.0),
                  (r'cidade', 1.0), (r'sitio', 1.0), (r'distrito', 1.0), (r'concelho', 1.0), (r'morada', 1.0), (r'filmes?', 1.0),
                  (r'cinemas?.+proximos?', 1.5), (r'filmes? nos? cinemas?', 2.0)],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/scrapper/movies/search',
        'service': 'CINEMA_SCRAPER',
        'words': [(r'filme', 1.0), (r'pelicula', 1.0), (r'video', 1.0), (r'procurar?', 1.0), (r'consultar?', 1.0), (r'filmes?\.(com|de|sobre)', 2.0)],
        'paramsRequired': {},
        'paramsOptional': {'genre':'MOVIE_GENRE', 'cast':'PERSON', 'producer':'PERSON', 'synopsis':'SYNOPSIS', 'age':'CARDINAL'},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': True
    },
    {
        'request': '/scrapper/movies/releases',
        'service': 'CINEMA_SCRAPER',
        'words': [(r'filme', 1.0), (r'pelicula', 1.0), (r'video', 1.0), (r'estreias?', 1.0), (r'novo', 1.0), (r'estrear', 1.0),
                  (r'lancamento', 1.0), (r'filmes? a sair', 1.5), (r'filmes?.+estrear', 2.0), (r'filmes?.+estreias?', 2.0),
                  (r'filmes?.+novos?', 1.0)],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/scrapper/movies/details',
        'service': 'CINEMA_SCRAPER',
        'words': [(r'filme', 1.0), (r'pelicula', 1.0), (r'video', 1.0), (r'detalhes', 1.0), (r'informac(ao|oes)', 1.0),
                  (r'sobre', 1.0), (r'casting', 1.0), (r'ator', 1.0), (r'produtor', 1.0), (r'realizador', 1.0), (r'tipo', 1.0),
                  (r'genero', 1.0), (r'categoria', 1.0), (r'sinopse', 1.0), (r'historia', 1.0), (r'restricao', 1.0), (r'criancas', 1.0),
                  (r'adultos', 1.0), (r'sobre o filme', 1.0), (r'informac(ao|oes) do filme', 2.0)],
        'paramsRequired': {"movie":'WORK OF ART'},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/scrapper/sessions/by_duration',
        'service': 'CINEMA_SCRAPER',
        'words': [(r'sess(ao|oes)', 1.0), (r'sess(ao|oes)', 1.0), (r'exibic(ao|oes)', 1.0), (r'duracao', 1.0), (r'tempo', 1.0),
                  (r'tamanho', 1.0), (r'demora', 1.0), (r'extensao', 1.0), (r'minutos', 1.0), (r'horas?', 1.0), (r'sess(ao|oes) ate', 1.0),
                  (r'sess(ao|oes) com menos', 2.5)],
        'paramsRequired': {"duration":'TIME'},
        'paramsOptional': {'date':'DATE', 'start_time':'TIME', 'end_time':'TIME'},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/scrapper/sessions/next_sessions',
        'service': 'CINEMA_SCRAPER',
        'words': [(r'sess(ao|oes)', 1.0), (r'exibic(ao|oes)', 1.0), (r'proxim[oa]s', 1.0), (r'agora', 1.0), (r'seguintes?', 1.0),
                  (r'prestes', 1.0), (r'proximas? sess(ao|oes)', 2.5), (r'proximas? exibic(ao|oes)', 2.5)],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/scrapper/sessions/by_movie',
        'service': 'CINEMA_SCRAPER',
        'words': [(r'sess(ao|oes)', 1.0), (r'exibic(ao|oes)', 1.0), (r'filme', 1.0), (r'sess(ao|oes) dos? filmes?', 2.0)],
        'paramsRequired': {"movie":'WORK OF ART'},
        'paramsOptional': {'date':'DATE', 'start_time':'TIME', 'end_time':'TIME'},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False
    },
    {
        'request': '/scrapper/sessions/by_date',
        'service': 'CINEMA_SCRAPER',
        'words': [(r'sess(ao|oes)', 1.0), (r'exibic(ao|oes)', 1.0), (r'proximas', 1.0), (r'dia', 1.0), (r'horas?', 1.0),
                  (r'inicio', 1.0), (r'fim', 1.0), (r'hoje', 1.0), (r'amanha', 1.0)],
        'paramsRequired': {},
        'paramsOptional': {'date':'DATE', 'start_time':'TIME', 'end_time':'TIME'},
        'locationParam': {'search_term':'GPE', 'lat':'', 'lon':''},
        'canRequestWithoutParams': False,
        'needAtLeastOneOptionalParam': False
    },
    # RS
    {
        'request': '/solver',
        'service': 'RS',
        'words': [(r'problemas?', 1.0), (r'avarias?', 1.0)],
        'paramsRequired': {},
        'paramsOptional': {},
        'locationParam': {},
        'canRequestWithoutParams': True,
        'needAtLeastOneOptionalParam': False
    }
]
