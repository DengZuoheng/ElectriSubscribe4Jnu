#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
import server.settings


settings.configure(DATABASES = server.settings.DATABASES)

from subscriber import models 
from django.http import HttpResponse

import json

import os

#os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'

def test(request):
    
    l=list(models.Record.objects.all())
    
    ret={'abc':[]}
    for item in l:
        ret['abc'].append({
            'dorm':str(item.dorm),
            })
    if(request==None):
        return json.dumps(ret)
    return HttpResponse(json.dumps(ret))
    """
    m=models.Record()
    m.set(dorm='3313')
    print(m.dorm)
    """
    pass

if __name__ == '__main__':
    print(test(None))