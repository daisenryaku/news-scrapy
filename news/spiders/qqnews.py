# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.dealstr import cleanStr,getStr
from news.dealurl import getUrl,filterUrl,textUrl
import time

class qqnewsSpider(scrapy.Spider):
    name = "qq"
    allowed_domains = ["qq.com"]
    start_urls = (
        'http://www.qq.com/',
    )
    filter = ['v.qq','piao.qq','astro','gongyi','rudao','yunqi']

    def parse(self, response):
        match1 = '//*[@id="navBeta"]/div[1]/div/a/@href'
        match2 = '//*[@id="navBeta"]/div[1]/div/strong/a/@href'
        urls = getUrl(response, match1, match2, self.filter)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse2)

    def parse2(self, response):
        suffix = ['html','htm']
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
            title = title.split('_')[0]
            #过滤]符号
            title = title.split(u'\u3011')[-1]
            item['news_title'] = title
        else:
            item['news_title'] = ''
        #abstract & body
        abstract = response.xpath('//p/text()').extract()
        if abstract != []:
            x = [cleanStr(i) for i in abstract if len(i.replace(' ','')) > 20]
            if x != []:
                item['news_abstract'] = getStr(x)
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
