
from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from models import * 
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
def form(request):
    return render_to_response(
            'form.html',
            context_instance=RequestContext(request))

def subcribe_action(request):
    pass