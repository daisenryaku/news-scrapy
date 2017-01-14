# -*- coding: utf-8 -*-
import scrapy


class ChinaSpider(scrapy.Spider):
    name = "china"
    allowed_domains = ["china.com.cn"]
    start_urls = (
        'http://www.china.com.cn/',
    )

    def parse(self, response):
        pass
