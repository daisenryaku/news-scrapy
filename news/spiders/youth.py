# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.dealstr import cleanStr,getStr
from news.dealurl import getUrl,filterUrl,textUrl
import time


class YouthSpider(scrapy.Spider):
    name = "youth"
    allowed_domains = ["youth.cn"]
    start_urls = (
        'http://www.youth.cn/',
        'http://edu.youth.cn/',
        'http://mil.youth.cn/',
        'http://pinglun.youth.cn/',
        'http://health.youth.cn/',
        'http://news.youth.cn/',
        'http://finance.youth.cn/',
        'http://www.youth.cn/',
    )
    filter = []

    def parse(self, response):
        suffix = ['htm']
        urls = textUrl(response,suffix)
        urls = filterUrl(urls,self.filter)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse3)

    def parse3(self,response):
        item = NewsItem()
        #url
        item['news_url'] = response.url
        #title
        title = response.xpath('//title/text()').extract()
        if title != []:
            title = title[0].replace(',','').replace(' ','').replace('\n','')
            #标题过滤
            title = title.split('_')[0].split('-')[0].split('|')[0]
            title = title.split(u'\u3011')[-1]
            item['news_title'] = title
        else:
            item['news_title'] = ''
        #abstract & body
        abstract = response.xpath('//p/text()').extract()
        if abstract != []:
            x = [cleanStr(i) for i in abstract if len(i.replace(' ','')) > 20]
            if x != []:
                text = getStr(x)
                if u'\u3011' in text:
                    item['news_abstract'] = text.split(u'\u3011')[-1]
                elif u'\uff09' in text:
                    item['news_abstract'] = text.split(u'\uff09')[-1]
                else:
                    item['news_abstract'] = text
                #新闻正文
                s = ''
                for i in x:
                    s += i
                item['news_body'] = s.replace(' ','').replace('\n','').replace('\t','')
            else:
                item['news_abstract'] = title
                item['news_body'] = title
        else:
            item['news_abstract'] = title
            item['news_body'] = title
        #time
        item['news_time'] = time.time()
        yield item
