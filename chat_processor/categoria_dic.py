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
    }
]
