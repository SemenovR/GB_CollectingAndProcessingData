# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItemSJ

class SjruSpider(scrapy.Spider):
    search_value = 'python'
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = [f'https://www.superjob.ru/vacancy/search/?keywords={search_value}&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancy_items = response.xpath("//a[starts-with(@class,'icMQ_ _1QIBo')]/@href").extract()
        for link in vacancy_items:
            yield response.follow('https://www.superjob.ru' + link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract_first()
        salary_script = response.xpath("//div[@class='_1Tjoc _3C60a Ghoh2 UGN79 _1XYex']/script[@type='application/ld+json']/text()").extract_first()
        url = response.request.url
        source = 'superjob.ru'
        yield JobparserItemSJ(name=name, salary_script=salary_script, url=url, source=source)

