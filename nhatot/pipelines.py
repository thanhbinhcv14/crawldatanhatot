# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os

class NhatotPipeline:
    def process_item(self, item, spider):
        return item
    
# đưa ra file csv
class CsvWriterPipeline:
    def open_spider(self, spider):
        self.file = open('nhatotdata.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['name', 'price', 'address', 'price_m2', 'rooms', 'house_type','land_type', 'legal_document', 'pty_characteristics', 'land_area_m2','descriptions'])

    def process_item(self, item, spider):
        self.writer.writerow([item['name'], item['price'], item['address'], item['price_m2'], item['rooms'], item['house_type'],item['land_type'], item['legal_document'], item['pty_characteristics'], item['land_area_m2'],item['descriptions']])
        return item

    def close_spider(self, spider):
        self.file.close()
# Lưu dl vô mongodb
class MongoDBPipeline:
    def __init__(self):
        mongo_host = os.getenv('MONGO_HOST', 'localhost')  # Mặc định là 'localhost'
        self.client = MongoClient(f'mongodb://{mongo_host}:27017/')
        self.db = self.client['nhatot']
        self.collection = self.db['projects']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()