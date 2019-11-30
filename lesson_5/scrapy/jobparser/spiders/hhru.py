# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItemHH

class HhruSpider(scrapy.Spider):
    search_value = 'python'
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [f'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text={search_value}&showClusters=true']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancy_items = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_items:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@data-qa='vacancy-title']//text()").extract_first()
        salary_from = response.xpath("//span[@itemprop='baseSalary']//meta[@itemprop='minValue']/@content").extract_first()
        salary_to = response.xpath("//span[@itemprop='baseSalary']//meta[@itemprop='maxValue' or @itemprop='value']/@content").extract_first()
        url = response.request.url
        source = 'hh.ru'
        yield JobparserItemHH(name=name, salary_from=salary_from, salary_to=salary_to, url=url, source=source)





