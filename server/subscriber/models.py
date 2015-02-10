#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
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

