# -*- coding: utf-8 -*-
import scrapy


class ChinadailySpider(scrapy.Spider):
    name = "chinadaily"
    allowed_domains = ["cn.chinadaily.com.cn"]
    start_urls = (
        'http://www.cn.chinadaily.com.cn/',
    )

    def parse(self, response):
        pass
