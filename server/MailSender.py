#!/usr/bin/env python  
#-*- coding: utf-8 -*-

import smtplib
import sys
import unittest
#import email.mime.text
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

import time
import datetime

class MailSender:
    def __init__(self,__addr,__pw):
        self.addr = __addr
        self.pw = __pw
        self.status = True

        host = 'smtp.'+__addr.split('@')[-1]
        port = 25
        self.server = smtplib.SMTP(host,port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()

        try:
            self.server.login(self.addr,self.pw)
        except:
            self.status = False

    def __del__(self):
        self.server.quit()

    def send(self,addr_to,subject,content):
        #addr_to为对方地址,subject为主题,content为正文
        if self.status == True :
            msg = MIMEText(content,_charset='utf-8')
            msg['To'] = addr_to
            msg['Subject'] = subject 
            try:      
                self.server.sendmail(self.addr,addr_to,msg.as_string())
            except:
                self.status = False
                raise Exception

#测试类
class MailSenderTestCase(unittest.TestCase):
    def testSendaMail(self):
        sender=MailSender('dengzuoheng@gmail.com','ainsophaur000')
        sender.send('2470423627@qq.com','给邓作恒发邮件测试','测试邮件正文')
        sender.send('chenrenzhan@gmail.com','给陈仁湛发邮件测试','测试邮件正文\n第二行')
        #会进垃圾箱

if __name__=='__main__':unittest.main()
