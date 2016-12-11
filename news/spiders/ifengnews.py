# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import time

class IfengnewsSpider(scrapy.Spider):
    name = "ifengnews"
    allowed_domains = ["ifeng.com"]
    start_urls = (
        'http://www.ifeng.com/',
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
        filter = ['house','cp.ifeng','v.ifeng','jiu.ifeng','tuangou','phtv.ifeng','vip.v','vc.ifeng','fo.ifeng','jiangjia']
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
        head_url = response.xpath('//html/body/div/div/ul/li/a/@href').extract()
        head_url.append(response.url)
        head_url = self.filterUrl(head_url)
        for url in head_url:
            yield scrapy.Request(url, callback=self.parse2)

    def parse2(self, response):
        #li
        data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//li/a')]
        data = [i for i in data if len(i) == 2 and len(i[1])>9 and 'shtml' in i[0].split('.')]
        #h2
        h2_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h2/a')]
        h2_data = [i for i in h2_data if len(i) == 2 and len(i[1])>9 and 'shtml' in i[0].split('.')]
        for i in h2_data:
            data.append(i)
        #h3
        h3_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h3/a') ]
        h3_data = [i for i in h3_data if len(i) == 2 and len(i[1])>9 and 'shtml' in i[0].split('.')]
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
            title = title.split(u'\u2014')[0].split('_')[0].split('|')[0]
            item['news_title'] = title
        else:
            item['news_title'] = ''
        #abstract & body
        abstract = response.xpath('//p/text()').extract()
        if abstract != []:
            x = [self.cleanStr(i) for i in abstract if len(i.replace(' ','')) > 20]
            x = [i for i in x if 'Copyright' not in i]
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
