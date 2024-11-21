import scrapy


class MyscraperSpider(scrapy.Spider):
    name = "myscraper"
    allowed_domains = ["www.nhatot.com"]
    start_urls = ["https://www.nhatot.com/mua-ban-bat-dong-san?gidzl=6oCyGhnj7b4UE3r1ktKML1uxCq6dU19N13ip4gHo5mq3QcDEf2b3MmetP1_uAKzT2sHjIZUNUn8dlM0VNG"]

    def parse(self, response):
        pass
