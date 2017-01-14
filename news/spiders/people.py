# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.dealstr import cleanStr,getStr
from news.dealurl import getUrl,filterUrl,textUrl
import time


class PeopleSpider(scrapy.Spider):
    name = "people"
    allowed_domains = ["people.com.cn"]
    start_urls = (
        'http://www.people.com.cn/',
    )
    filter = []

    def parse(self, response):
        pass
