# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

class JobparserItemHH(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    salary_from = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(int))
    salary_to = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(int))
    url = scrapy.Field(output_processor=TakeFirst())
    source = scrapy.Field(output_processor=TakeFirst())

class JobparserItemSJ(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    salary_from = scrapy.Field()    # Обрабатывается в JobparserPipeline
    salary_to = scrapy.Field()      # Обрабатывается в JobparserPipeline
    salary_script = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    source = scrapy.Field(output_processor=TakeFirst())
