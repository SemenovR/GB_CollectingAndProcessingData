# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    return value

def cleaner_address(value):
    return value.strip()

class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_address))
    text = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(int))
    currency = scrapy.Field(output_processor=TakeFirst(), input_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
