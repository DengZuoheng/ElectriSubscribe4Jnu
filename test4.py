#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pycurl
import pyquery
import datetime
import urllib
import StringIO
import re
import datetime
 
buf = StringIO.StringIO()
buf1=StringIO.StringIO()

html=None;
string = "GGG"

def callback(data):
    f=open('abc.html','w')
    f.write(data.getvalue())
    string="HHH"
    #print(data.decode('utf-8'))
def callback1(data):
    pass

"""
c = pycurl.Curl() 
hosturl = 'http://www.google.com/'
c.setopt(pycurl.URL, hosturl)#设置目标URL
c.setopt(pycurl.WRITEFUNCTION, callback)#设置回调
c.setopt(pycurl.CONNECTTIMEOUT, 5)
c.setopt(pycurl.TIMEOUT, 8)
c.setopt(pycurl.PROXY, '127.0.0.1:8118')#设置代理
c.perform() #执行请求
c.close() #关闭
"""

c=pycurl.Curl()

c.setopt(c.CONNECTTIMEOUT,5)
c.setopt(c.TIMEOUT,8)
c.setopt(c.COOKIEFILE,'')
c.setopt(pycurl.PROXY, '127.0.0.1:8888')
c.setopt(c.FAILONERROR,True)

c.setopt(c.HTTPHEADER,[
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

values={
    "__EVENTARGUMENT":"",
    "__EVENTTARGET":"",
    "__EVENTVALIDATION":"/wEWBQLz+M6SBQK4tY3uAgLEhISACwKd+7q4BwKiwImNC7oxDnFDxrZR6l5WlUJDrpGZXrmN",
    "__LASTFOCUS":"",
    "__VIEWSTATE":"/wEPDwULLTE5ODQ5MTY3NDlkZM4DISokA1JscbtlCdiUVQMwykIc",
    "__VIEWSTATEGENERATOR":"C2EE9ABB",
    "ctl01":"",
    #"hidtime":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "hidtime":"",
    "txtname":"3313",
    "txtpwd":"",
}



post_data=urllib.urlencode(values)
print(post_data)
c.setopt(c.URL, 'http://202.116.25.12/login.aspx')
c.setopt(c.POSTFIELDS, post_data)
c.setopt(pycurl.WRITEFUNCTION,callback1)#设置回调
c.perform()
c.setopt(c.POST,False)
c.setopt(c.URL, 'http://202.116.25.12/default.aspx')
c.setopt(pycurl.WRITEFUNCTION, buf.write)#设置回调
c.perform()

default_aspx_html=buf.getvalue().decode('utf-8')

meter=0
print(">>>>>>>>>>>>>>")
res=re.findall(u"\[电表\]\|(\d+)",default_aspx_html)
if(len(res)!=0):
    meter=res[0].decode('utf-8')


pq=pyquery.PyQuery(default_aspx_html)
__EVENTVALIDATION=pq('#__EVENTVALIDATION').val()

__VIEWSTATE=pq('#__VIEWSTATE').val()

today=datetime.date.today()
delta=datetime.timedelta(days=-30)
oldday=today+delta
txtstarOld=str(oldday)
txtstar=str(today)

value2={
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
post_data2=urllib.urlencode(value2)
#print(post_data2)
c.setopt(c.POSTFIELDS, post_data2)
c.setopt(c.POST,True)
c.setopt(c.URL, 'http://202.116.25.12/default.aspx')
c.setopt(pycurl.WRITEFUNCTION, buf1.write)#设置回调
"""
c.setopt(c.HTTPHEADER,[
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
    'X-Requested-With: XMLHttpRequest',
    ])
"""
c.perform()

str3=buf1.getvalue()


res=re.findall(u"box\.__27\.setValue\(\"(\d+\.\d+)\"\)",str3)
print(res[0])

print(string)
print "status code: %s" % c.getinfo(pycurl.HTTP_CODE)
print(string)
if (200==c.getinfo(pycurl.HTTP_CODE)):
    print(u"成功")
c.close()
print(string)
callback(buf)



