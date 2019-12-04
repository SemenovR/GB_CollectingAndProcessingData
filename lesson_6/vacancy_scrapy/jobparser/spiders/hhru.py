# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItemHH
from scrapy.loader import ItemLoader

class HhruSpider(scrapy.Spider):
    search_value = 'python'
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [f'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text={search_value}&showClusters=true']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="bloko-button HH-Pager-Controls-Next HH-Pager-Control"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancy_items = response.xpath('//a[@class="bloko-link HH-LinkModifier"]/@href').extract()
        for link in vacancy_items:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItemHH(), response=response)
        loader.add_value('source', 'hh.ru')
        loader.add_value('url', response.url)
        loader.add_xpath('name', '//h1[@data-qa="vacancy-title"]//text()')
        loader.add_xpath('salary_from', '//span[@itemprop="baseSalary"]//meta[@itemprop="minValue"]/@content')
        loader.add_xpath('salary_to', '//span[@itemprop="baseSalary"]//meta[@itemprop="maxValue" or @itemprop="value"]/@content')
        yield loader.load_item()
