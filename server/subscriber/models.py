#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pycurl
from django.db import models
from MailSender import MailSender
import datetime
import StringIO
import json
import urllib
# Create your models here.

class Record(models.Model):
    #宿舍号
    dorm=models.CharField(max_length=4)
    #反馈方式, 比如短信, 邮件, 目前只支持邮件
    feedback_type=models.CharField(max_length=8,default='mail')
    #报警联系方式, 如果上面的反馈方式是邮件, 这里就是邮件地址, 如此类推
    alarm_mode=models.CharField(max_length=128)
    #报警下限, 则剩余电量低于这个值就会报警
    lower_limit=models.FloatField(blank=True,default=30.00)
    #回调, 报警是除了反馈, 还能设置url进行回调
    #回调为GET方法,带有参数
    #参数为json, 形同{'drom':'3313','remain':'140.10'}
    callback=models.URLField(blank=True)
    #剩余电量
    current_remain=models.FloatField(blank=True,default=30.00)

    def set(self,
        dorm='',
        feedback_type='',
        alarm_mode='',
        lower_limit='',
        callback='',
        current_remain=''):
        self.dorm=dorm
        self.feedback_type=feedback_type
        self.alarm_mode=alarm_mode
        self.lower_limit=lower_limit
        self.callback=callback
        self.current_remain=current_remain

    def warning(self):
        if(self.current_remain<=self.lower_limit):
            self.feedback()
            self.callback()

    def feedback(self):
        if(self.feedback_type=='mail'):

            mail_sender=MailSender("dengzuoheng@gmail.com","ainsophaur000")
            import datetime
            now=datetime.datetime.now()
            str_now= now.strftime("%Y-%m-%d %H:%M:%S")
            str_subject=now.strftime("%Y-%m-%d")+u"电费到期通知"
            str_context=u"截"+str_now+u"您的宿舍"+self.dorm+u"的剩余电量仅剩"+self.current_remain+u"度.请注意充值"
            str_context+="\n\n---\n"
            str_context+="技术支持:暨大开发者社区"
            mail_sender.send(self.alarm_mode,str_subject,str_context)

    def callback(self):
        buf = StringIO.StringIO()
        c=pycurl.Curl()
        url=self.callback
        value={
            'dorm':self.dorm,
            'reamin':self.current_remain,
        }
        data=urllib.urlencode(value)
        c.setopt(pycurl.URL, url+'?'+data)
        c.setopt(pycurl.CONNECTTIMEOUT,5)
        c.setopt(pycurl.TIMEOUT,8)
        c.setopt(pycurl.COOKIEFILE,'')
        c.setopt(pycurl.FAILONERROR,True)     
        c.setopt(pycurl.WRITEFUNCTION, buf.write)#设置回调
        c.perform()

class Error(models.Model):
    what=models.TextField(blank=True)

    def json(self):
        try:
            ret=json.loads(self.what)
            return ret
        except Exception as e:
            return {'what':self.what}
    def __unicode__(self):
        return {
            'id':self.id,
            'what':self.what,
        }