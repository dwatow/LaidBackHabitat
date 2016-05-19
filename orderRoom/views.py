# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response, get_list_or_404
from .models import Employee
import time
import datetime

# Create your views here.
def index(request):
    return render_to_response('index.html', locals())

def test(request, link_value):
    display_text = 'AAAAA'
    return render_to_response('test.html', locals())

'''
def order_room(request):
    from_str = request.POST.get('from', '')
    to_str = request.POST.get('to', '')
    if from_str and to_str:
        from_year, from_month, from_day = request.POST.get('from', '').split('-')
        from_datetime = datetime.datetime(int(from_year), int(from_month), int(from_day))  

        to_year, to_month, to_day = request.POST.get('to', '').split('-')
        to_datetime = datetime.datetime(int(to_year), int(to_month), int(to_day))  

        total_day = abs((to_datetime - from_datetime).days)
        return HttpResponse('客人您於' + str(from_datetime.date()) + '到' + str(to_datetime.date()) + '，有訂房。<br />祝你這' + str(total_day) + '天玩得開心。')
    else:
        return HttpResponse('您要兩個時都輸入，才能知道您訂房的狀況。')
        #return HttpResponseRedirect('/')
'''        