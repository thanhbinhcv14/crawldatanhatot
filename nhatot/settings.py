# settings.py

import os

BOT_NAME = "nhatot"

SPIDER_MODULES = ["nhatot.spiders"]
NEWSPIDER_MODULE = "nhatot.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
   "nhatot.pipelines.CsvWriterPipeline": 300,
   'nhatot.pipelines.MongoDBPipeline': 400,
}

# Cấu hình MongoDB từ biến môi trường
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', '27017')
MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'nhatot_database')

MONGO_URI = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/'

# Các cấu hình khác...
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://www.nhatot.com',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
}

ROTATING_PROXY_LIST = ['http://proxy1.com', 'http://proxy2.com', ...]
