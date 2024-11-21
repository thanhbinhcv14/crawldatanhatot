import scrapy
import re
from nhatot.items import NhatotItem


class CrawlingSpider(scrapy.Spider):
        name = 'crawlnhatot'  # Tên của spider
        custom_settings = {
            'DOWNLOAD_DELAY': 2,  # Đặt độ trễ giữa các yêu cầu
            'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Số yêu cầu đồng thời
            'AUTOTHROTTLE_ENABLED': True,  # Bật tính năng tự động điều chỉnh tốc độ
            'AUTOTHROTTLE_START_DELAY': 5,
            'AUTOTHROTTLE_MAX_DELAY': 60,
            'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        }
        # Mở web để lấy link dự án
        def start_requests(self):
            urls = 'https://www.nhatot.com/mua-ban-bat-dong-san?gidzl=qbdB2nUczYdHJimD4xtn9z1CpWKEkVTpoqoOK0-wgYBEJfa5NEpmSyWSp0KExF9odnhDKcJmnWiJ4AZu80'
            for i in range(1, 150):  # Thay đổi số trang nếu cần
                start_urls = f"{urls}&page={i}"
                yield scrapy.Request(url=start_urls, callback=self.parse)

        # Lấy link dự án
        def parse(self, response):
            for project in response.xpath('//div[4]/div/div[1]/ul/div/li/a/@href').getall():  # Sửa dùng getall để lấy nhiều link
                item = NhatotItem()
                item['link'] = project  # Lấy từng link dự án

                # Gọi đến hàm parse_get_info để lấy thông tin chi tiết của từng dự án
                yield scrapy.Request(
                    url=response.urljoin(item['link']),
                    callback=self.parse_get_info,
                    meta={'item': item}
                )

        # Lấy thông tin chi tiết của dự án
        def parse_get_info(self, response):
            item = response.meta['item']

            # Lấy tên nhà
            item['name'] = response.xpath('//div[4]/div/div[2]/div/h1/text()').get(default='Không có tên')
            
            # Lấy giá nhà
            item['price'] = response.xpath('//div/div[2]/div/div[2]/div[1]/div/b/text()').get(default='Không có giá')
            
            # Lấy địa chỉ
            item['address'] = response.xpath('//div[2]/div/div[3]/div[1]/span[2]/text()').get(default='Không có địa chỉ')
            
            # Lấy giá/m2
            item['price_m2'] = response.xpath('//span[@itemprop="price_m2"]/text()').get(default='Không có giá/m2')
            
            # Lấy số phòng
            item['rooms'] = response.xpath('//span[@itemprop="rooms"]/text()').get(default='Không có thông tin số phòng')
            
            # Lấy loại nhà
            item['house_type'] = response.xpath('//span[@itemprop="house_type"]/text()').get(default='Không có loại nhà')

            # Lấy loại nhà
            item['land_type'] = response.xpath('//span[@itemprop="land_type"]/text()').get(default='Không rõ loại hình đất')
            
            # Lấy giấy tờ pháp lý
            item['legal_document'] = response.xpath('//span[@itemprop="property_legal_document"]/text()').get(default='Không có giấy tờ pháp lý')
            
            # Lấy đặc điểm
            item['pty_characteristics'] = response.xpath('//span[@itemprop="pty_characteristics"]/text()').get(default='Không có đặc điểm')
            
            # Lấy diện tích
            item['land_area_m2'] = response.xpath('//span[@itemprop="size"]/text()').get(default='Không có diện tích')

            #Lấy mô tả
            item['descriptions'] = response.xpath('//p[@class="styles_adBody__vGW74"]/text()').get(default='Không có mô tả')

            
            yield item