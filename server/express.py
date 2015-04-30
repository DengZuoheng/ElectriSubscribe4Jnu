#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
查电费精简版
@author: 邓作恒
@mail: dengzuoheng@gmail.com
@date: 2015/4/30
"""
import urllib2
import cookielib
import re
import urllib
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

def express_local(dorm):
    cookie = cookielib.CookieJar()  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))  
    login_url = 'http://202.116.25.12/login.aspx'
    login_values = {
            "__EVENTVALIDATION":"/wEWBQLz+M6SBQK4tY3uAgLEhISACwKd+7q4BwKiwImNC7oxDnFDxrZR6l5WlUJDrpGZXrmN",
            "__VIEWSTATE":"/wEPDwULLTE5ODQ5MTY3NDlkZM4DISokA1JscbtlCdiUVQMwykIc",
            "ctl01":"",
            "txtname":dorm,
        }
    login_post_data = urllib.urlencode(login_values) 
    opener.open(urllib2.Request(login_url, login_post_data))
    default_url = 'http://202.116.25.12/default.aspx'
    response = opener.open(urllib2.Request(default_url))
    html = response.read().decode('utf-8')
    ajax_values={
            '__41_value':'00900200',
            '__box_ajax_mark':'true',
            '__EVENTVALIDATION':re.findall(r'id="__EVENTVALIDATION" value="(.*?)"',html)[0],
            '__VIEWSTATE':re.findall(r'id="__VIEWSTATE" value="(.*?)"',html)[0],
        }
    ajax_post_data=urllib.urlencode(ajax_values)
    js_response = opener.open(urllib2.Request(default_url, ajax_post_data))
    fin_data = js_response.read()
    return re.findall(u"box\.__27\.setValue\(\"(\d+\.\d+)\"\)",fin_data)[0]
   
def mail_me(remain,alert_value):
    addr = 'dengzuoheng@gmail.com'
    pw = 'ainsophaur000'
    host = 'smtp.gmail.com'
    port = 25
    server  = smtplib.SMTP(host,port)
    server.ehlo()
    server.starttls()
    self.ehlo()
    server.login(addr,pw)
    content = ''
    msg = MIMEText(content,_charset='utf-8')
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    if((int(remain)<=alert_value)):
        subject = u'[import!][电费报警] %s %s'%(remain,date)
    else:
        subject = u'[电费报告] %s %s'%(remain,date)
    msg['To'] = addr
    msg['Subject'] = subject 
    server.sendmail(addr,addr,msg.as_string())

def main():
    mail_me(express_local('3313'),240)

if __name__=='__main__':
    main()