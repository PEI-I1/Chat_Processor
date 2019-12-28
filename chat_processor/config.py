import os

urls = {
    'API_ENDPOINT': os.getenv('API_ENDPOINT', "http://127.0.0.1:5000"),
    'FS_SCRAPER': os.getenv('FS_SCRAPER', 'http://127.0.0.1:5002'),
    'CINEMA_SCRAPER': os.getenv('CINEMA_SCRAPER', 'http://127.0.0.1:5003'),
    'RS': os.getenv('RS', 'http://127.0.0.1:5004'),
    'REDIS': {'host': os.getenv('REDIS_HOST', 'localhost'), 'port': os.getenv('REDIS_PORT', 6379)}
}
