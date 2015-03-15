#!/usr/bin/env python
# -*- coding: utf-8 -*-
#trigger.py
from django.conf import settings
import server.settings
from MailSender import MailSender
settings.configure(DATABASES = server.settings.DATABASES)

#import subscriber.models
from subscriber.models import Record, Error
import service
import threading
import json 

class SnaperThread(threading.Thread):
    def __init__(self,record):
        print(record.dorm)
        threading.Thread.__init__(self)
        self.record=record

    def run(self):
        import os
        import sys

        from django.core.wsgi import get_wsgi_application

        os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
        application = get_wsgi_application()
        from subscriber.models import Record, Error
        try:
            
            remain=service.get_remain(self.record.dorm)        
            record=Record.objects.get(id=self.record.id)         
            record.current_remain=remain
            record.save()
        
        except Exception as e:
           
            what={
                'what':str(e),
                'id':str(self.record.id),
                'dorm':str(self.record.dorm),
            }
            what_str=json.dumps(what)
            error=Error(what=what_str)
            error.save()
        

#检查所有定制
def check_all():
    query_set=Record.objects.all()
    for item in query_set:
        item.warning()

def snap_all():
    thread_list=[]
    query_set=Record.objects.all()
    for item in query_set:
        thread_list.append(SnaperThread(item))
        thread_list[-1].start()

    for item in thread_list:
        item.join()

def confirm_to_me():

    mail_sender=MailSender("dengzuoheng@gmail.com","ainsophaur000")
    now = datetime.datetime.now() 
    str_confirm_subject=str_now+u"电费检查完成"
    str_now= now.strftime("%Y-%m-%d %H:%M:%S")
    str_confirm_contex=''
    try:
        query_set=list(Error.objects.all())
        if(0<=len(query_set)):
            str_confirm_contex+=u"以下异常账号:\n"
            for item in query_set:
                data=item.json()
                str_confirm_contex+=u'dorm:'+data['dorm']+u' id:'+data['id']+u' what:'+data['what']+'\n'
        else:
            str_confirm_contex+=u"没有异常"

        mail_sender.send("dengzuoheng@gmail.com",str_confirm_subject,str_confirm_contex)
        Error.objects.all().delete()
    except:
        pass