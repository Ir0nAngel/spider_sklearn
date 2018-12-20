# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SklearnFuncItem(scrapy.Item):
    func_name = scrapy.Field()


class SklearnArgItem(scrapy.Item):
    arg_name = scrapy.Field()
    sklearn_func_id = scrapy.Field()
    arg_value = scrapy.Field()
    arg_doc = scrapy.Field()
