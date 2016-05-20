# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response, get_list_or_404
from . import models
import time
import datetime

# Create your views here.
def index(request):
    return render_to_response('index.html', locals())

def test(request, link_value):
    display_text = 'AAAAA'
    return render_to_response('test.html', locals())

def reservations(request):
    if 'customer_id' in request.GET:
        cid = request.GET['customer_id']
        customer = models.Customer.objects.filter(c_id=cid)[0]
        return HttpResponse(customer.c_name + 'is a customer<br />query any thing');
    else:
        raise Http404("data does not exist")

def checkout(request):
    if 'cleaner_id' in request.GET:
        id = request.GET['cleaner_id']
        obj = models.Cleaner.objects.filter(id=id)[0]
        return HttpResponse(obj.cl_name + 'is a cleaner<br /> query be able to clean room');

    if 'employee_id' in request.POST:
        id = request.GET['employee_id']
        employee = models.Employee.objects.filter(id=id)[0]
        return HttpResponse(employee.e_name + 'is a employee<br />checkout for customer<br />change order status');

def checkin(request):
    if 'employee_id' in request.GET:
        id = request.GET['employee_id']
        employee = models.Employee.objects.filter(id=id)[0]
        return HttpResponse(employee.e_name + 'is a employee<br />query can checkin room');

    if 'employee_id' in request.POST:
        id = request.GET['employee_id']
        employee = models.Employee.objects.filter(id=id)[0]
        return HttpResponse(employee.e_name + 'is a employee<br />get pay from customer<br />change order status');
    elif 'cleaner_id' in request.POST:
        id = request.GET['cleaner_id']
        obj = models.Cleaner.objects.filter(id=id)[0]
        return HttpResponse(obj.cl_name + 'is a cleaner<br />clear room be used checkin');



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