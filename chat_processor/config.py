import os

API_ENDPOINT = os.getenv('API_ENDPOINT', "http://127.0.0.1:5000")
FS_SCRAPER = os.getenv('FS_SCRAPER', 'http://127.0.0.1:5002')
CINEMA_SCRAPER = os.getenv('CINEMA_SCRAPER', 'http://127.0.0.1:5003')
RS = os.getenv('RS', 'http://127.0.0.1:5004')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
PARAM_THRESHOLD = 2
INACTIVE_TIME = 5 #minutes
NOTIFICATION_TASK_INTERVAL = 1 #minutes

urls = {
    'API_ENDPOINT': API_ENDPOINT,
    'FS_SCRAPER': FS_SCRAPER,
    'CINEMA_SCRAPER': CINEMA_SCRAPER,
    'RS': RS
}
