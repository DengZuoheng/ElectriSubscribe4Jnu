
from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from models import * 
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json

# Create your views here.
def form(request,error_id='0'):
    try:
        context={}
        if('0'!=error_id):
            error=Error.objects.get(id=error_id)
            context['error_item']=json.loads(error.what)

        return render_to_response(
                'form.html',
                context,
                context_instance=RequestContext(request))
    except:
        return render_to_response(
                'form.html',
                context_instance=RequestContext(request))

def subcribe_action(request):
    input_dorm=request.POST['input-dorm']
    input_mail=request.POST['input-mail']
    try:
        record=Record(dorm=input_dorm,alarm_mode=input_mail)
        record.save()
        return HttpResponseRedirect('/success')
    except Exception as e:
        error=Error(what=unicode(e))
        error.save()
        return HttpResponseRedirect(reverse('library.views.form', args=[error.id]))

def success(request):
    context={
        'back_href':'/index/',
    }
    return render_to_response(
            'success.html',
        )