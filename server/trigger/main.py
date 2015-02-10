#!/usr/bin/env python
# -*- coding: utf-8 -*-
#main.py
import threading
import time
import datetime
import trigger

def set_timer(hour,minute=0,second=0,callback):
    now=datetime.datetime.now()
    t1=now.hour*3600+now.minute*60+now.second
    t2=hour*3600+minute*60+second
    if(t1<t2):
        global timer
        timer = threading.Timer(t2-t1, callback, [])
        timer.start()
    elif(t2<t1):
        global timer
        timer = threading.Timer(24*3600-t1+t2, callback, [])
        timer.start()
    else:#t1=t2
        global timer
        timer = threading.Timer(1, callback, [])
        timer.start()

def main():
    #执行其他操作
    trigger.snap_all()#先抓下左右剩余电量存起来
    trigger.check_all()#然后检查时候需要报警
    #最后
    set_timer(hour=0,callback=main)
    pass


if __name__ == '__main__': 
    set_timer(hour=0,callback=main)
    