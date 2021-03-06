#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created Date: 2019-04-09
# Project     : crawl data of bidcenter.com.cn 

import sys
import requests
import random
from lxml import etree
import sqlite3
import hashlib
import getbaiduurls
import datetime
print("The python version is : ",sys.version)

def bidcenter_by_url(url):
        
    #Get random user anget aginst being blocked by the site
    headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cookie': 'bidguid=09d0ae31-90e9-4d91-bae3-6a0a4cd44bdc; _uab_collina=155287009327192506718305; _umdata=G5D18F32E82CECF330D494AB726F58604B97D70; BIDCTER_USERNAME=UserName=13810757300; bidguidnew=5ed59a72-79db-4ecb-ae6a-faa09ae4c0b9; bidcurrKwdDiqu=kwd=èªç©º&diqu=35; Hm_lvt_9954aa2d605277c3e24cb76809e2f856=1552889439,1553218279,1553218350,1553758161; keywords==%e5%9b%bd%e7%94%b5; Hm_lpvt_9954aa2d605277c3e24cb76809e2f856=1554970538',
                'Referer': 'https://search.bidcenter.com.cn/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    #url = "https://search.bidcenter.com.cn/search?keywords=港务 可视化&type=1"
    #url = "https://search.bidcenter.com.cn/search?keywords=%E6%B8%AF%E5%8A%A1%20%E5%8F%AF%E8%A7%86%E5%8C%96&type=1"
    url = url
    print("handling url: ",url)
    req = requests.get(url,headers=headers)
    #print(req.text)

    #解析单网页
    etree_data = etree.HTML(req.content)

    #获取数据主体
    tbody_datas = etree_data.xpath("//tbody//tr")
    # //*/tr[*]
    #tbody_datas = etree_data.xpath("//*/tr[*]")

    #print(type(tbody_datas))
    bid_datas = tbody_datas[0:-1]
    #print(type(bid_datas))
    #print("-------------------------------------------------------------------------------------------")
    #print(len(bid_datas))
    #print(etree.tostring(tbody_datas[1],pretty_print=True))
    #print("-------------------------------------------------------------------------------------------")
    #print("".join(tbody_datas[0].xpath("string(//tr/td[@class='zb_title']/a)")))
    #bid1 = tbody_datas[1]
    #print(bid1.xpath("string(//tr/td[@class='zb_title']/a)"))
    #print("".join(tbody_datas[0].xpath("//tr/td[@class='zb_title']/a/text()")))

    #for bid_data in bid_datas:
        #print("-------------------------------------------------------------------------------------------")
        #print(etree.tostring(bid_data,pretty_print=True))
        #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #print("".join(bid_data.xpath("//td[@class='zb_title']/a/text()")))
        #print("".join(bid_data.xpath("//tr/td[@class='list_area']/a/text()")))
        #print("".join(bid_data.xpath("//td[@class='list_time']/text()")))
        #bid = {}
        #bid['title'] = bid_data.xpath("string(//tr/td[@class='zb_title']/a)").strip()
        #print(bid['title'] )
        #print(bid_data.xpath("string(//tr/td[@class='zb_title']/a)").strip())
        #break
    conn = sqlite3.connect('bid_datas.db')
    cur = conn.cursor()
    insert_sql_str = '''
                    INSERT INTO bid_info (bid_md5_url , bid_title , bid_prov , bid_create_date , bid_url , baidu_urls , bid_content ,
                                        src_url , bid_data_status , crawl_time , baidu_time , email_time)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?);

                    '''
    bid_md5_url=""
    bid_title=""
    bid_prov=""
    bid_create_date=""
    bid_url=""
    baidu_urls=""
    bid_content=""
    src_url="https://www.bidcenter.com.cn/"
    bid_data_status=""
    crawl_time=""
    baidu_time=""

    for idx,bid_data in enumerate(bid_datas):
        print(idx,"----------------------------------------")
        print(etree.tostring(bid_data,method='html',pretty_print=True,encoding='Unicode'))
        print(idx,"++----------------------------------------")
        #bid_title = etree.XPath("")
        #print(bid_data.xpath("//tr/td[@class='zb_title']")[idx].xpath("string(//td/a)").strip())
        #print(bid_data.xpath("string(//td[@class='zb_title']/a)").strip())
        #print(bid_data.xpath("string(td[@class='zb_title']/a/text())").strip())
        #bid_title_data = bid_data.xpath("//tr/td[@class='zb_title']/a")[idx]
        #print(etree.tostring(bid_title_data,method='html',pretty_print=True,encoding='unicode'))
        #print(bid_title_data.xpath("string(.)").strip())
        #print(bid_data.xpath("//tr/td[@class='zb_title']/a")[idx].xpath("string(.)").strip())
        bid_title = bid_data.xpath("//tr/td[@class='zb_title']/a")[idx].xpath("string(.)").strip()
        bid_prov = bid_data.xpath("//tr/td[@class='list_area']/a/text()")[idx].strip()
        bid_create_date = bid_data.xpath("//tr/td[@class='list_time']/text()")[idx].strip()
        bid_url = "https:"+bid_data.xpath("//tr/td[@class='zb_title']/a/@href")[idx].strip()
        bid_md5_url = hashlib.md5(bid_url.encode('utf-8')).hexdigest()
        bid_data_status = 'ready2email' # ready2baidu ; ready2email ; done
        baidu_urls = getbaiduurls.get_baidu_urls_by_keyword(bid_title)
        # print(bid_title)
        # print(bid_prov)
        # print(bid_create_date)
        # print(bid_url)
        # print(bid_md5_url)
        # if idx == 1:
        #     break
        except_keywords=["维修","监控","代理","运维"]
        #last two week dates
        last_two_week_dates = [(datetime.date.today()-datetime.timedelta(days=x)).isoformat() for x in range(0,7)]        

        if (not any(x in bid_title for x in except_keywords )) and  bid_create_date in last_two_week_dates:
            
            bid_data_list = [bid_md5_url , bid_title , bid_prov , bid_create_date , bid_url , ','.join(baidu_urls) , "" , src_url , bid_data_status , datetime.datetime.now(), datetime.datetime.now() , ""]
            print(bid_data_list)

            try:
                cur.execute(insert_sql_str,bid_data_list)
            except sqlite3.IntegrityError:
                print("sqlite3.IntegrityError: column bid_md5_url is not unique")
                print("已经存在的招标实体： ",bid_md5_url,bid_title)
            conn.commit()
            print(">>>>>>>>>>>>>>>>>>>>>>")
    conn.close()

if __name__ == '__main__':
    
    #搜索关键词--供应链王帆提供
    #search_keywords=["供应链","系统","技术服务","TMS","OMS","船运服务","物流","平台","运输","化工园区","智慧园区","智慧物流","电子运单","船舶运输","港务 可视化","危化品 IT","危化品 物流","危险货物道路运输安全","危 道路运输安全","危化品装卸运输监管平台","危 运输监管平台","油 租船"]
    search_keywords=["TMS","电子运单","船舶运输","港务 可视化","危化品 IT","危化品 物流","危险货物道路运输安全","危 道路运输安全","危化品装卸运输监管平台","危 运输监管平台","油 租船"]
    
    url = "https://search.bidcenter.com.cn/search?keywords={0}&type=1"
    urls = [url.format(x) for x in search_keywords]
    for url in urls:
        
        bidcenter_by_url(url)