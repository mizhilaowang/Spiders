#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import random
from lxml import etree

#Get random user anget aginst being blocked by the site
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'zh-CN,zh;q=0.9',
             'Cookie': 'bidguid=09d0ae31-90e9-4d91-bae3-6a0a4cd44bdc; _uab_collina=155287009327192506718305; _umdata=G5D18F32E82CECF330D494AB726F58604B97D70; BIDCTER_USERNAME=UserName=13810757300; bidguidnew=5ed59a72-79db-4ecb-ae6a-faa09ae4c0b9; bidcurrKwdDiqu=kwd=èªç©º&diqu=35; Hm_lvt_9954aa2d605277c3e24cb76809e2f856=1552889439,1553218279,1553218350,1553758161; keywords==%e5%9b%bd%e7%94%b5; Hm_lpvt_9954aa2d605277c3e24cb76809e2f856=1554970538',
             'Referer': 'https://search.bidcenter.com.cn/',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

url = "https://search.bidcenter.com.cn/search?keywords=%E6%B8%AF%E5%8A%A1%20%E5%8F%AF%E8%A7%86%E5%8C%96&type=1"

req = requests.get(url,headers=headers)
#print(req.text)

#解析单网页
etree_data = etree.HTML(req.content)

#标题
tbody_datas = etree_data.xpath("//tbody//tr")
bid_datas = tbody_datas[0:-1]
print(len(bid_datas))
for bid_data in bid_datas:
    print("-------------------------------------------------------------------------------------------")
    print(etree.tostring(bid_data,pretty_print=True))
    print("+++++++++++")
    print(bid_data.xpath("//td[@class='zb_title']/a/text()"))
    print(bid_data.xpath("//tr/td[@class='list_area']/a/text()"))
    print(bid_data.xpath("//td[@class='list_time']/text()"))
    break
