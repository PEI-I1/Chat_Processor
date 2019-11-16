cat = [
    {
        'request': 'linhas_apoio',
        'service': 'FS_SCRAPER',
        'words': ['linhas','linha','apoio','assunto','número','contacto','contactos','empresa','empresas','aderir','informações','adicionais','informação','adicional','serviços','chamada','chamadas','ligar','falar',"assistente"],
        'params': ['SUBJECT'],
        'canRequestWithoutParams': True
    },
    {
        'request': 'phone_model',
        'service': 'FS_SCRAPER',
        'words': ['modelos','modelo','telemóvel','telemóveis'],
        'params': ['PRODUCT'],
        'canRequestWithoutParams': False
    },
    {
        'request': 'brand_phones',
        'service': 'FS_SCRAPER',
        'words': ['marca','marcas','comprar','telemóvel','telemóveis','preço'],
        'params': ['ORG'],
        'canRequestWithoutParams': False
    },
    {
        'request': 'top_phones',
        'service': 'FS_SCRAPER',
        'words': ['top','telemóvel','telemóveis','melhores','link'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'promo_phones',
        'service': 'FS_SCRAPER',
        'words': ['promoções','promoção','desconto','descontos','barato','baratos','telemóvel','telemóveis'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'new_phones',
        'service': 'FS_SCRAPER',
        'words': ['novidades','novos','telemóvel','telemóveis','recente','recentes'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'ofer_phones',
        'service': 'FS_SCRAPER',
        'words': ['oferta','telemóvel','telemóveis'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'prest_phones',
        'service': 'FS_SCRAPER',
        'words': ['prestações','prestação','telemóvel','telemóveis'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'points_phones',
        'service': 'FS_SCRAPER',
        'words': ['ponto','pontos','telemóvel','telemóveis'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'phones_by_price',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preço','telemóvel','telemóveis'],
        'params': ['MONEY', 'MONEY'],
        'canRequestWithoutParams': False
    },
    {
        'request': 'all_wtf',
        'service': 'FS_SCRAPER',
        'words': ['tarifários','telemóvel','wtf'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'stores_by_zone',
        'service': 'FS_SCRAPER',
        'words': ['loja','lojas','zona'],
        'params': ['GPE'],
        'canRequestWithoutParams': False
    },
    {
        'request': 'store_address',
        'service': 'FS_SCRAPER',
        'words': ['morada','loja','lojas'],
        'params': ['FAC'],
        'canRequestWithoutParams': False
    },
    {
        'request': 'packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'fiber_packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes', 'fibra'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'satelite_packages',
        'service': 'FS_SCRAPER',
        'words': ['pacotes', 'satelite', 'satélite'],
        'params': [],
        'canRequestWithoutParams': True
    },
    {
        'request': 'packages_service',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preço','pacote','pacotes'],
        'params': ['PACKAGE'],
        'canRequestWithoutParams': False
    },
    {
        'request': 'packages_price',
        'service': 'FS_SCRAPER',
        'words': ['ordenar','preço','pacote','pacotes'],
        'params': ['MONEY', 'MONEY'],
        'canRequestWithoutParams': False
    }
]
