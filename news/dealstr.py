# -*- coding: utf-8 -*-
import scrapy

def cleanStr(s,filter=[]):
    basic_filter = [' ','\n',',',u'\u3000',']','\r']
    for i in filter:
        basic_filter.append(i)
    for i in basic_filter:
        s = s.replace(i,'')
    return s

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

#获得摘要
def getStr(s,filter=[]):
    result = ''
    flag = 0
    for i in s:
        for j in filter:
            if j in i:
                flag = 1
        if flag == 0:
            result += i
        if i[-1] == u'\u3002' or i[-1] == u'\uff1f':
            break
    return result
