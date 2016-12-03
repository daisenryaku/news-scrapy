# -*- coding: utf-8 -*-
import csv

class NewsPipeline(object):
    def process_item(self, item, spider):
        if item['news_title'] != '' and item['news_abstract'] != '' and len(item['news_title']) > 6 :
            with open('title.csv', 'a') as csvfile:
                spamwriter = csv.writer(csvfile,dialect='excel')
                title = item['news_title'].encode('utf-8')
                url = item['news_url']
                abstract = item['news_abstract'].encode('utf-8')
                spamwriter.writerow([title,url,abstract])
            return item
