# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class financeItem(scrapy.Item):
    fcode = scrapy.Field()
    name = scrapy.Field()
    market = scrapy.Field()
    price = scrapy.Field()
    priceTime = scrapy.Field()
    diffyesterdayPer = scrapy.Field()
    diffyesterdayPrice = scrapy.Field()
    trade = scrapy.Field()
    date = scrapy.Field()
    def __unicode__(self):
        return repr(self).decode('unicode_escape')