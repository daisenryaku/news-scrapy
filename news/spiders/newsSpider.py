# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import re
import numpy as np

class TitleSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["www.163.com","baby.163.com","edu.163.com","ent.163.com",
                       "house.163.com","money.163.com","news.163.com","play.163.com","tech.163.com",
                       "sports.163.com","travel.163.com","war.163.com"
                       ]
    start_urls = [
    "http://www.163.com","http://baby.163.com","http://edu.163.com","http://ent.163.com",
    "http://house.163.com","http://money.163.com","http://news.163.com","http://play.163.com",
    "http://tech.163.com","http://sports.163.com","http://travel.163.com","http://war.163.com",
    ]

    def parse(self, response):
        item = NewsItem()
        #li
        data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//li/a')]
        data = [i for i in data if np.size(i) == 2 and 'html' in i[0].split('.')]
        #h2
        h2_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h2/a')]
        h2_data = [i for i in h2_data if np.size(i) == 2 and 'html' in i[0].split('.')]
        for i in h2_data:
            data.append(i)
        #h3
        h3_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h3/a')]
        h3_data = [i for i in h3_data if np.size(i) == 2 and 'html' in i[0].split('.')]
        for i in h3_data:
            data.append(i)
        #url
        urls = [i[0] for i in data]
        for url in urls:
            yield scrapy.Request(url,meta={'item':item}, callback=self.parse2)

    def parse2(self,response):
        item = response.meta['item']
        #url
        item['news_url'] = response.url
        #title
        title = response.xpath('//title/text()').extract()
        if title != []:
            title = title[0].replace(',','').replace(' ','').replace('\n','')
            title = title.split('_')[0]
            item['news_title'] = title
        else:
            item['news_title'] = ''
        #abstract
        abstract = response.xpath('//p/text()').extract()
        if abstract != []:
            x = [i for i in abstract if len(i) > 20 and u'\uff08' not in i]
            if x != []:
                item['news_abstract'] = x[0].replace('\n','').replace(' ','').replace(',','')
            else:
                item['news_abstract'] = title
        else:
            item['news_abstract'] = title
        yield item
