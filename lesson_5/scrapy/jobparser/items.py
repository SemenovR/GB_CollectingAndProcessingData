# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItemHH(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary_from = scrapy.Field()
    salary_to = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()

class JobparserItemSJ(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary_from = scrapy.Field()
    salary_to = scrapy.Field()
    salary_script = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
