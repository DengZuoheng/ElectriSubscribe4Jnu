#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
邓作恒
dengzuoheng@gmail.com
2015/2/9
"""
import pycurl
import pyquery
import datetime
import urllib
import StringIO
import re
import datetime
import StringIO
import json
import unittest

def get_remain(dorm):
    try:
        return use_local_request(dorm)
    except:
        return None

def use_publicAPI(dorm):
    buf = StringIO.StringIO()
    
    c=pycurl.Curl()
    url=r'http://api.jnutong.com/power.php?room='+str(dorm)
    c.setopt(pycurl.CONNECTTIMEOUT,5)
    c.setopt(pycurl.TIMEOUT,8)
    c.setopt(pycurl.COOKIEFILE,'')
    c.setopt(pycurl.FAILONERROR,True)
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEFUNCTION, buf.write)#设置回调
    c.perform()
    json_str=buf.getvalue()
    try:
        match=re.search(r'(\{.+)',json_str)#暨南通的返回数据头部有点乱码,用正则去掉
        data=json.loads(match.group())
        return data['remain']
    except:
        return None
        
#自己模拟登陆去获取剩余电量
def use_local_request(dorm):
    buf1 = StringIO.StringIO()
    buf2 = StringIO.StringIO()
    buf3 = StringIO.StringIO()

    c=pycurl.Curl()

    c.setopt(pycurl.CONNECTTIMEOUT,5)
    c.setopt(pycurl.TIMEOUT,8)
    c.setopt(pycurl.COOKIEFILE,'')
    #c.setopt(pycurl.PROXY, '127.0.0.1:8888')#port8888可用于监视
    c.setopt(pycurl.FAILONERROR,True)
    #header其实是可以不要的
    c.setopt(pycurl.HTTPHEADER,[
        'Accept: text/html, application/xhtml+xml, */*',
        'Accept-Encoding: gzip, deflate',
        'Accept-Language: en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Cache-Control: no-cache',
        'Connection: Keep-Alive',
        'Content-Type: application/x-www-form-urlencoded',
        'Host: 202.116.25.12',
        'Referer: http://202.116.25.12/login.aspx',
        'Proxy-Connection: Keep-Alive',
        'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        ])

    login_values={
        #其实hidtime也是随便的
        "__EVENTARGUMENT":"",
        "__EVENTTARGET":"",
        "__EVENTVALIDATION":"/wEWBQLz+M6SBQK4tY3uAgLEhISACwKd+7q4BwKiwImNC7oxDnFDxrZR6l5WlUJDrpGZXrmN",
        "__LASTFOCUS":"",
        "__VIEWSTATE":"/wEPDwULLTE5ODQ5MTY3NDlkZM4DISokA1JscbtlCdiUVQMwykIc",
        "__VIEWSTATEGENERATOR":"C2EE9ABB",
        "ctl01":"",
        "hidtime":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "hidtime":"",
        "txtname":dorm,
        "txtpwd":"",
    }
    login_post_data=urllib.urlencode(login_values)
    c.setopt(pycurl.URL, 'http://202.116.25.12/login.aspx')
    c.setopt(pycurl.POSTFIELDS, login_post_data)
    c.setopt(pycurl.WRITEFUNCTION,buf1.write)#设置回调
    c.perform()
    if (200!=c.getinfo(pycurl.HTTP_CODE)):
        return None

    #此时登陆应该完成了
    #下一步是提取电表号
    c.setopt(pycurl.POST,False)
    c.setopt(pycurl.URL, 'http://202.116.25.12/default.aspx')
    c.setopt(pycurl.WRITEFUNCTION, buf2.write)#设置回调
    c.perform()
    if (200!=c.getinfo(pycurl.HTTP_CODE)):
        return None

    #需要分析html
    html=buf2.getvalue().decode('utf-8')
    meter=0
    res=re.findall(u"\[电表\]\|(\d+)",html)
    if(len(res)!=0):
        meter=res[0].decode('utf-8')
        f = open('abcdef.txt','w')
        f.write(html)
        #准备ajax获取剩余电量的参数
        pq=pyquery.PyQuery(html)

        __EVENTVALIDATION=pq('#__EVENTVALIDATION').val()
        
        __VIEWSTATE=pq('#__VIEWSTATE').val()

        #txtstarOld必须比txtstar早, 不然返回数据会没有剩余电量
        today=datetime.date.today()
        delta=datetime.timedelta(days=-30)#虽然不知道什么含义, 不过一律弄到30天前好了
        oldday=today+delta
        txtstarOld=str(oldday)
        txtstar=str(today)

        ajax_values={
            #实际上只查剩余电量的话, 只有__41_value,__bok_ajax_mark,__EVENTVALIDATION,__VIEWSTATE是必须的
            '__12_disable_select_row_indexs':'',
            '__12_last_value':u'[电表]|'+meter,
            '__12_value':u'[电表]|'+meter,
            '__41_disable_select_row_indexs':'',
            '__41_last_value':'00000000',
            '__41_value':'00900200',
            '__43_selectedRows':'',
            '__44_selectedRows':'',
            '__45_selectedRows':'',
            '__box_ajax_mark':'true',
            '__box_page_state_changed':'false',
            '__EVENTARGUMENT':'',
            '__EVENTTARGET':u'RegionPanel1$Region2$GroupPanel1$ContentPanel1$DDL_监控项目',
            '__EVENTVALIDATION':__EVENTVALIDATION,
            '__LASTFOCUS':'',
            '__VIEWSTATE':__VIEWSTATE,
            '__VIEWSTATEGENERATOR':'CA0B0334', 
            'hidpageCurrentSize':'1',
            'hidpageCurrentSize2':'1',
            'hidpageCurrentSize3':'1',
            'hidpageSum':'1',
            'hidpageSum2':'4',
            'hidpageSum3':'5',
            'PandValue':'10',
            'RegionPanel1$Region1$GroupPanel2$Grid1$Toolbar1$pagesize':'1',
            'RegionPanel1$Region1$GroupPanel2$Grid2$Toolbar3$pagesize2':'1',
            'RegionPanel1$Region1$GroupPanel2$Grid3$Toolbar2$pagesize3':'1',
            'tqid':'',
            'tqsort':'',
            'RegionPanel1$Region3$ContentPanel3$txtstarOld':txtstarOld,
            'RegionPanel1$Region3$ContentPanel3$txtstar':txtstar,
            'RegionPanel1$Region3$ContentPanel3$tb_ammeterNumb':u'[电表]'+meter,
        }
        ajax_post_data=urllib.urlencode(ajax_values)

        c.setopt(pycurl.POSTFIELDS, ajax_post_data)
        c.setopt(pycurl.POST,True)
        c.setopt(pycurl.URL, 'http://202.116.25.12/default.aspx')
        c.setopt(pycurl.WRITEFUNCTION, buf3.write)#设置回调
        c.perform()
        if (200!=c.getinfo(pycurl.HTTP_CODE)):
            return None

        fin_data=buf3.getvalue()
        res=re.findall(u"box\.__27\.setValue\(\"(\d+\.\d+)\"\)",fin_data)
        if(0!=len(res)):
            return res[0]
        else:
            return None
    else:
        return None



#单元测试
class ServiceTestCase(unittest.TestCase):
    def test_local_request(self):
        print(u"use local request")
        print(use_local_request('3313'))

if __name__ == '__main__': 
    unittest.main()