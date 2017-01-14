# -*- coding: utf-8 -*-
import scrapy


class PeopleSpider(scrapy.Spider):
    name = "people"
    allowed_domains = ["people.com.cn"]
    start_urls = (
        'http://www.people.com.cn/',
    )

    def parse(self, response):
        pass
