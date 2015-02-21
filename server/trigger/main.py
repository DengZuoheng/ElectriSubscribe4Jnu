#!/usr/bin/env python
# -*- coding: utf-8 -*-
#main.py
import threading
import time
import datetime
#import trigger.trigger

def set_timer(timer,hour,minute=0,second=0,callback=None,callback_parm=[]):
    now=datetime.datetime.now()
    t1=now.hour*3600+now.minute*60+now.second
    t2=hour*3600+minute*60+second
    if(t1<t2):
        timer = threading.Timer(t2-t1, callback, callback_parm)
        timer.start()
    elif(t2<t1):
        timer = threading.Timer(24*3600-t1+t2, callback, callback_parm)
        timer.start()
    else:#t1=t2
        timer = threading.Timer(1, callback, callback_parm)
        timer.start()

def main(timer):
    #执行其他操作
    trigger.trigger.snap_all()#先抓下左右剩余电量存起来
    trigger.trigger.check_all()#然后检查时候需要报警
    trigger.trigger.confirm_to_me()#再然后, 给我自己发一份确认
    #最后
    set_timer(timer=timer,hour=0,callback=main,callback_parm=[timer,])
    pass



if __name__ == '__main__':
    timer=None
    set_timer(timer=timer,hour=0,callback=main,callback_parm=[timer,])
    