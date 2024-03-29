# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BestsellerItem(scrapy.Item):
    ranking = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    score = scrapy.Field()
    introduce = scrapy.Field()