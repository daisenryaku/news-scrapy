# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import time

class _163newsSpider(scrapy.Spider):
    name = "163news"
    allowed_domains = ["163.com"]
    start_urls = [
    "http://www.163.com","http://baby.163.com","http://edu.163.com","http://ent.163.com",
    "http://house.163.com","http://money.163.com","http://news.163.com","http://play.163.com",
    "http://tech.163.com","http://sports.163.com","http://travel.163.com","http://war.163.com",
    ]

    def getStr(self,s):
        result = ''
        for i in s:
            if u'\u539f\u6807\u9898' in i:
                pass
            else:
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
        return [x for x in urls if 'goal' not in x]

    def parse(self, response):
        #li
        data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//li/a')]
        data = [i for i in data if len(i) == 2 and len(i[1])>9 and 'htm' in i[0].split('.') or 'html' in i[0].split('.')]
        #h2
        h2_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h2/a')]
        h2_data = [i for i in h2_data if len(i) == 2 and 'html' in i[0].split('.')]
        for i in h2_data:
            data.append(i)
        #h3
        h3_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h3/a')]
        h3_data = [i for i in h3_data if len(i) == 2 and 'html' in i[0].split('.')]
        for i in h3_data:
            data.append(i)
        #url
        urls = [i[0] for i in data]
        urls = self.filterUrl(urls)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse2)

    def parse2(self,response):
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
        #abstract
        abstract = response.xpath('//p/text()').extract()
        if abstract != []:
            x = [self.cleanStr(i) for i in abstract if len(i.replace(' ','')) > 20]
            if x != []:
                item['news_abstract'] = self.getStr(x)
            else:
                item['news_abstract'] = title
        else:
            item['news_abstract'] = title
        #time
        item['news_time'] = time.time()
        yield item
