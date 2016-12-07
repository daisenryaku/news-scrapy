# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import time

class qqnewsSpider(scrapy.Spider):
    name = "qqnews"
    allowed_domains = ["qq.com"]
    start_urls = (
        'http://www.qq.com/',
    )

    def getStr(self,s):
        result = ''
        for i in s:
            result += i
            if i[-1] == u'\u3002' or i[-1] == u'\uff1f':
                break
        return result

    def cleanStr(self,s):
        filter = [' ','\n',',',u'\u3000',']','\r']
        for i in filter:
            s = s.replace(i,'')
        return s

    def filterUrl(self, urls):
        filter = ['v.qq','piao.qq','astro','gongyi','rudao','yunqi']
        result = []
        for x in urls:
            flag = 0
            for f in filter:
                if f in x:
                    flag = 1
                    break
            if flag == 0:
                result.append(x)
        return result

    def parse(self, response):
        #获得首页导航链接，继续爬
        head_url = response.xpath('//*[@id="navBeta"]/div[1]/div/a/@href').extract()
        head_url.append(response.url)
        strong_url = response.xpath('//*[@id="navBeta"]/div[1]/div/strong/a/@href').extract()
        for i in strong_url:
            head_url.append(i)
        head_url = self.filterUrl(head_url)
        for url in head_url:
            yield scrapy.Request(url, callback=self.parse2)

    def parse2(self, response):
        #li
        data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//li/a')]
        data = [i for i in data if len(i) == 2 and len(i[1])>9 and 'htm' in i[0].split('.') or 'html' in i[0].split('.')]
        #h2
        h2_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h2/a')]
        h2_data = [i for i in h2_data if len(i) == 2 and len(i[1])>9 and 'htm' in i[0].split('.') or 'html' in i[0].split('.')]
        for i in h2_data:
            data.append(i)
        #h3
        h3_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h3/a')]
        h3_data = [i for i in h3_data if len(i) == 2 and len(i[1])>9 and 'htm' in i[0].split('.') or 'html' in i[0].split('.')]
        for i in h3_data:
            data.append(i)
        #url
        urls = [i[0] for i in data]
        urls = self.filterUrl(urls)
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
            item['news_title'] = title
        else:
            item['news_title'] = ''
        #abstract & body
        abstract = response.xpath('//p/text()').extract()
        if abstract != []:
            x = [self.cleanStr(i) for i in abstract if len(i.replace(' ','')) > 20]
            if x != []:
                item['news_abstract'] = self.getStr(x)
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
