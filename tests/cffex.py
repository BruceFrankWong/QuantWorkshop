# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import requests
from xml.etree.ElementTree import parse, Element


# response = requests.get('http://www.cffex.com.cn/jycs/')

response = requests.get('http://www.cffex.com.cn/sj/jycs/202011/04/index.xml?id=40')

print(response.content.decode("utf-8"))

doc = parse(response.content.decode("utf-8"))
root = doc.getroot()

if __name__ == '__main__':
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)

    parser.parse("movies.xml")
