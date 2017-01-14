# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.dealstr import cleanStr,getStr
from news.dealurl import getUrl,filterUrl,textUrl
import time

class FirefoxSpider(scrapy.Spider):
    name = "firefox"
    allowed_domains = ["firefoxchina.cn"]
    start_urls = (
        'http://www.firefoxchina.cn/',
    )
    filter = []

    def parse(self, response):
        pass
