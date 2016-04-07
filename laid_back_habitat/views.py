# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
def index(request):
    return render_to_response('index.html',locals())
    
def order_room(request):
    if 'order' in request.POST:
        year = request.POST.get('year', '')
        month = request.POST.get('month', '')
        day = request.POST.get('day', '')
        return HttpResponse('客人您於'+year+'年'+month+'月'+day+'日'+'，有訂房。')
    else:
        HttpResponse('您要訂的房間已滿。')
        #return HttpResponseRedirect('/')