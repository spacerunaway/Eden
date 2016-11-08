# -*- coding: utf-8 -*-
'''
Created on 2016年10月18日
C:\Python27\Lib\site-packages\scrapy\cmdline.py
http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
http://aosabook.org/en/index.html
@author: spacerunaway
'''
import scrapy
from bs4 import BeautifulSoup
from quotesbot.items import financeItem
from scrapy.selector import Selector
import re
import datetime

class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://info.finance.yahoo.co.jp/ranking/?kd=1&mk=1&tm=d&vl=a',
        'http://info.finance.yahoo.co.jp/ranking/?kd=2&mk=1&tm=d&vl=a',
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }
        item = financeItem()

        sel = Selector(response)
        table = soup.findAll("table",{"class":"rankingTable"})[0]
        rows = table.findAll("tr")
        for row in rows:
            cols = row.findAll("td")
            cols = [ele.text.strip() for ele in cols]
            item['fcode'] = cols[1] if cols else ""
            item['market'] = cols[2] if cols else ""
            item['name'] = cols[3] if cols else ""
            item['priceTime'] = cols[4] if cols else ""
            item['price'] = cols[5] if cols else ""
            item['diffyesterdayPer'] = cols[6] if cols else ""
            item['diffyesterdayPrice'] = cols[7] if cols else ""
            item['trade'] = cols[8] if cols else ""
            item['date'] = datetime.datetime.today()+ datetime.timedelta(hours=1)

            yield item

        # 次のページへのリンクが入った <リンク> を取得する
        next_page_link = soup.find(class_="ymuiPagingBottom")
        next_page_link = soup.find(class_="ymuiPagingBottom", text=re.compile(u"次へ"))
        next_page_link = soup.find(text=u'次へ')
        next_page_link = "" if next_page_link is None else next_page_link.parent

        if not next_page_link:
            yield
        elif 'href' in next_page_link.attrs:
            # 次のページが見つからなかったので終了
            yield scrapy.Request(next_page_link.get("href"))

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

