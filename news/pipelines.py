# -*- coding: utf-8 -*-
import csv

class NewsPipeline(object):
    def __init__(self):
        with open('news.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile,dialect='excel')
            spamwriter.writerow(["标题","链接","摘要","时间"])
    def process_item(self, item, spider):
        if item['news_title'] != '' and item['news_abstract'] != '' and len(item['news_title']) > 9 :
            with open('news.csv', 'a') as csvfile:
                spamwriter = csv.writer(csvfile,dialect='excel')

                title = item['news_title'].encode('utf-8')
                url = item['news_url']
                abstract = item['news_abstract'].encode('utf-8')
                time = item['news_time']

                spamwriter.writerow([title,url,abstract,time])
            return item
