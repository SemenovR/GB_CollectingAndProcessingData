# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import json

class JobparserPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.vacancy252

    def close_spider(self, spider):
        self.client.close()

    def parse_sallary_hh(self, salary_from, salary_to):
        try:
            low = int(salary_from)
        except Exception:
            low = None
        try:
            high = int(salary_to)
        except Exception:
            high = None
        return (low, high)

    def parse_sallary_sj(self, salary_script):
        data = json.loads(salary_script)
        try:
            low = int(data['baseSalary']['value']['minValue'])
        except Exception:
            low = None
        try:
            high = int(data['baseSalary']['value']['maxValue'])
        except Exception:
            high = None
        return (low, high)

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary_from'], item['salary_to'] = self.parse_sallary_hh(item['salary_from'], item['salary_to'])
        elif spider.name == 'sjru':
            try:
                item['salary_from'], item['salary_to'] = self.parse_sallary_sj(item['salary_script'])
                del item['salary_script']
            except Exception as err:
                print(f'Error: {err}')

        collection = self.db[spider.name]
        collection.update_one({'url': item['url']}, {'$set': item}, upsert=True)

        return item
