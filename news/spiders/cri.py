# -*- coding: utf-8 -*-
import scrapy


class CriSpider(scrapy.Spider):
    name = "cri"
    allowed_domains = ["cri.cn"]
    start_urls = (
        'http://www.cri.cn/',
    )

    def parse(self, response):
        pass
