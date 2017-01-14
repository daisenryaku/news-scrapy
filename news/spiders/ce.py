# -*- coding: utf-8 -*-
import scrapy


class CeSpider(scrapy.Spider):
    name = "ce"
    allowed_domains = ["ce.cn"]
    start_urls = (
        'http://www.ce.cn/',
    )

    def parse(self, response):
        pass
