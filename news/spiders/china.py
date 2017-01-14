# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.dealstr import cleanStr,getStr
from news.dealurl import getUrl,filterUrl,textUrl
import time


class ChinaSpider(scrapy.Spider):
    name = "china"
    allowed_domains = ["china.com.cn"]
    start_urls = (
        'http://www.china.com.cn/',
    )

    def parse(self, response):
        pass
