# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/vodnyy_transport/katera_i_yahty?cd=1']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-page js-pagination-next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        add_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        for link in add_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//h3[@class="title item-description-title "]/text()')
        loader.add_xpath('address', '//span[@itemprop="address"]/text()')
        loader.add_xpath('text', '//div[@class="item-description-text"]/p/text()')
        loader.add_xpath('price', '//div[@class="price-value price-value_side-card"]/*/span[@itemprop="price"]/@content')
        loader.add_xpath('currency', '//div[@class="price-value price-value_side-card"]/*/span[@itemprop="priceCurrency"]/@content')
        loader.add_xpath('photos', '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        yield loader.load_item()
