# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NhatotItem(scrapy.Item):
    
    link = scrapy.Field()  # Đường dẫn dự án
    name = scrapy.Field()  # Tên dự án
    price = scrapy.Field()  # Giá nhà
    address = scrapy.Field()  # Địa chỉ
    price_m2 = scrapy.Field()  # Giá/m2
    rooms = scrapy.Field()  # Số phòng
    house_type = scrapy.Field()  # Loại nhà
    legal_document = scrapy.Field()  # Giấy tờ pháp lý
    pty_characteristics = scrapy.Field()  # Đặc điểm
    land_area_m2 = scrapy.Field()  # Diện tích
    descriptions = scrapy.Field() # Mô tả
    land_type = scrapy.Field() # loai hinh dat
    
