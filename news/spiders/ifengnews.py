# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.dealstr import cleanStr,getStr
from news.dealurl import getUrl,filterUrl,textUrl
import time

class IfengnewsSpider(scrapy.Spider):
    name = "ifeng"
    allowed_domains = ["ifeng.com"]
    start_urls = (
        'http://www.ifeng.com/',
    )
    filter = ['house','cp.ifeng','v.ifeng','jiu.ifeng','tuangou','phtv.ifeng','vip.v','vc.ifeng','fo.ifeng','jiangjia']

    def parse(self, response):
        match1 = '//html/body/div/div/ul/li/a/@href'
        urls = getUrl(response, match1, [], self.filter)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse2)

    def parse2(self, response):
        suffix = ['shtml']
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
            title = title.split(u'\u2014')[0].split('_')[0].split('|')[0]
            title = title.split(u'\u3011')[-1]
            item['news_title'] = title
        else:
            item['news_title'] = ''
        #abstract & body
        abstract = response.xpath('//p/text()').extract()
        if abstract != []:
            x = [cleanStr(i) for i in abstract if len(i.replace(' ','')) > 20]
            x = [i for i in x if 'Copyright' not in i]
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
