# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import hashlib

import scrapy


class ScrapylagouItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    address = scrapy.Field()
    salary = scrapy.Field()
    workYear = scrapy.Field()
    company = scrapy.Field()
    financeStage = scrapy.Field()

    def get_md5(self):
        m = hashlib.md5()
        m.update(str(self.__dict__).encode('utf-8'))
        return m.hexdigest()
