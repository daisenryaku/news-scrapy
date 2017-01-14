# -*- coding: utf-8 -*-
import scrapy

#Url过滤
def filterUrl(urls,filter):
    result = []
    for x in urls:
        flag = 0
        for f in filter:
            if f in x:
                flag = 1
                break
        if flag == 0:
            result.append(x)
    return result

#提取首页Url
def getUrl(response,match1,match2,filter):
    url_1 = response.xpath(match1).extract()
    url_1.append(response.url)
    if match2 != []:
        url_2 = response.xpath(match2).extract()
        url_1 += url_2
    #获取首页链接路径
    url_1 = filterUrl(set(url_1),filter)
    return url_1

def textUrl(response,suffix,match = ['//li/a','//h2/a','//h3/a']):
    data = []
    urls = []
    for i in match:
        data += [sel.xpath("text()""|@href").extract() for sel in response.xpath(i)]
    for s in suffix:
        urls += [i for i in data if len(i) == 2 and len(i[1])>9 and s in i[0].split('.')]
    urls = [i[0] for i in urls]
    return urls
