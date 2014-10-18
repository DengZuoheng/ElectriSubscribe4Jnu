#!/usr/bin/env python  
#-*- coding: utf-8 -*-
import urllib2
import json
import threading
import time
import datetime
from MailSender import MailSender

class PowerGetterThread(threading.Thread):
    def __init__(self,dorm,mail):
        threading.Thread.__init__(self)
        self.dorm=dorm
        self.mail=mail
    def run(self):
        basic_url="http://api.jnutong.com/power.php?room="
        url=basic_url+self.dorm
        global except_lst
        global send_lst
        global log
        try:
            response=urllib2.urlopen(url)
            str_json=response.read()
            if str_json=="error":
                mutex.acquire()
                except_lst.append({"dorm":self.drom,"mail":self.mail})
                mutex.release()
            elif len(str_json)<=4:
                print(str_json)
                mutex.acquire()
                except_lst.append({"dorm":self.drom,"mail":self.mail})
                mutex.release()
            else:
                str_json="{"+str_json[4:]
                obj=json.loads(str_json)
                mutex.acquire()
                log+="dorm:"+self.dorm+" mail:"+self.mail+" remain:"+obj['remain']+"\n"
                mutex.release()
                if float(obj['remain'])<90:
                    mutex.acquire()
                    send_lst.append({"dorm":self.dorm,"mail":self.mail,"remain":obj['remain']})
                    mutex.release()
        except:
            mutex.acquire()
            except_lst.append({"dorm":self.dorm,"mail":self.mail})
            mutex.release()

def get_target_lst():
    ret=[]
    ret.append({"dorm":"3301","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3303","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3305","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3307","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3309","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3311","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3313","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"33133","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3411","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3412","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3413","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3415","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3416","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3417","mail":"dengzuoheng@gmail.com"})
    ret.append({"dorm":"3418","mail":"dengzuoheng@gmail.com"})
    return ret

target_lst=[]
except_lst=[]
send_lst=[]
log=""
mutex=threading.Lock()

def main():
    while True:
        local_time=datetime.datetime.now() 
        if local_time.hour==2:
        #东9区3点开始
            #初始化
            global target_lst
            global except_lst
            global send_lst
            target_lst=[]
            except_lst=[]
            send_lst=[]
            log=""
            #开始
            target_lst=get_target_lst()
            thread_lst=[None]*len(target_lst)
            index=0;

            #创建线程
            for index in range(0,len(target_lst)):
                thread_lst[index]=PowerGetterThread(target_lst[index]['dorm'],target_lst[index]['mail'])
                thread_lst[index].start()

            #等待所有子线程结束
            for t in thread_lst:
                t.join()

            #检查有没异常
            if(len(except_lst)>0):
                thread_lst=[None]*len(except_lst)
                index=0
                for index in range(0,len(except_lst)):
                    thread_lst[index]=PowerGetterThread(except_lst[index]['dorm'],target_lst[index]['mail'])
                except_lst=[]
                for t in thread_lst:
                    t.start()
                for t in thread_lst:
                    t.join()

            #开始发邮件
            mail_sender=MailSender("dengzuoheng@gmail.com","ainsophaur000")
            now = datetime.datetime.now() 
            str_now= now.strftime("%Y-%m-%d %H:%M:%S")
            for item in send_lst:
                str_subject="电费到期通知"
                str_context="截"+str_now+"您的宿舍"+item['dorm']+"的剩余电量仅剩"+item['remain']+"度.请注意充值"
                str_context+="\n\n"
                str_context+="技术支持:暨大开发者社区"
                mail_sender.send(item['mail'],str_subject,str_context)

            #给我自己发确认邮件 
            str_confirm_subject=str_now+"电费检查完成"
            str_confirm_contex="似乎顺理跑完了一次\n"
            if(len(except_lst)>0):
                str_confirm_contex+="以下异常账号:\n"
                for item in except_lst:
                    str_confirm_contex+="dorm:"+item['dorm']+" mail:"+item['mail']+"\n以下日志"+log
            mail_sender.send("dengzuoheng@gmail.com",str_confirm_subject,str_confirm_contex)

            #结束后睡眠一个小时避开循环检查
            time.sleep(3600)
        else:
            #半小时一次
            time.sleep(1800)

            

if __name__=='__main__':main()