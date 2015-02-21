#!/usr/bin/env python
# -*- coding: utf-8 -*-
#trigger.py
import sys
import os
curdir=os.path.abspath(os.curdir)
#path=os.path.abspath(os.path.join(os.path.pardir,'subscriber\\'))
path=os.path.abspath(os.path.pardir)
sys.path.append(path)
print(sys.path)
#import subscriber.models
from subscriber.models import Record, Error
import service
import threading

class SnaperThread(threading.Thread):
    def __init__(self,record):
        threading.Thread.__init__(self)
        self.record=record

    def run(self):
        try:
            remain=service.get_remain(self.record.dorm)
            self.record.current_remain=remain
            self.record.save()
        except Exception as e:
            what={
                'what':str(e),
                'id':str(self.id),
                'dorm':str(selg.dorm),
            }
            what_str=json.dumps(what)
            error=Error(what=what_str)
            error.save()

#检查所有定制
def check_all():
    query_set=Record.objects.all()
    for item in query_set:
        item.warning()
    confirm_to_me()

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