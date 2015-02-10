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
from subscriber import models
#检查所有定制
def check_all():
    pass

def snap_all():
    pass

if __name__ == '__main__': 
    set_timer(hour=0,callback=main)