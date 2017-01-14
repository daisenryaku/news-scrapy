# -*- coding: utf-8 -*-
import scrapy


class FirefoxSpider(scrapy.Spider):
    name = "firefox"
    allowed_domains = ["firefoxchina.cn"]
    start_urls = (
        'http://www.firefoxchina.cn/',
    )

    def parse(self, response):
        pass
