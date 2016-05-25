# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response, get_list_or_404
from . import models
import time
import datetime
from django.core.exceptions import ObjectDoesNotExist


class BookingUnit:
    def __init__(self, str_room_from_data_to_data):
        self.room_name, from_date, to_date = str_room_from_data_to_data.split(':')
        
        from_year, from_month, from_day = from_date.split('-')
        self.from_datetime = datetime.datetime(int(from_year), int(from_month), int(from_day))  
    
        to_year, to_month, to_day = to_date.split('-')
        self.to_datetime = datetime.datetime(int(to_year), int(to_month), int(to_day))  

    def total_day(self):
        return abs((self.to_datetime - self.from_datetime).days)+1

    def every_night(self):
        every_night_list=[]
        for day in range(self.total_day()):
            curr_datetime = self.from_datetime + datetime.timedelta(days=day)
            every_night_list.append(curr_datetime)
        return every_night_list



# Create your views here.
def index(request):
    return render_to_response('index.html', locals())

def test(request):
    return render_to_response('test.html', locals())

def testGet(request):
    request_get = request.GET;
    good_list = request_get.getlist('good[]')
    str_out=''
    for booking in good_list:
        str_out+=booking['room'] + '<br />'

    return HttpResponse(good_list)



def query_room(request):
    curr_date = request.GET['today']
    
    curr_year, curr_month, curr_day = curr_date.split('-')
    curr_datetime = datetime.datetime(int(curr_year), int(curr_month), int(curr_day))  

    room_type_list = models.RoomType.objects.all()
    room_histogram={}
    for type in room_type_list:
        room_histogram[type.rt_name] = 0
    
    room_list = models.Room.objects.all()
    for room in room_list:
        room_histogram[room.room_type.rt_name] += 1
    
    booking_list = models.BookingRoom.objects.filter(over_night_date=curr_datetime)
    for booking_room in booking_list:
        curr_room_type = booking_room.room.room_type
        room_histogram[curr_room_type.rt_name] -= 1
        if room_histogram[curr_room_type.rt_name] < 0:
            room_histogram[curr_room_type.rt_name] = 0
    
    return render_to_response('BookingList.html', locals())

def booking_room(request):
    post_data = request.GET
    '''
    if 'booking_data' in post_data:
        test = post_data['booking_data']
        return HttpResponse(test);
    #c_id = post_data['customer_id']
    #customer = models.Customer.objects.filter(c_id=c_id)[0];
    
    #return HttpResponse(str(original_from.date()) + ", " + str(total_day));
    #return HttpResponse(str(original_from.date()) + ", " + str(next_from.date()));
    '''
    if 'customer_id' and \
       'customer_name' and \
       'customer_phone' and \
       'customer_address' in post_data and \
       'order_date' and\
       'booking[]' in post_data:
        
        target_customer=obj_cus = models.Customer()
        try:
            old_customer = models.Customer.objects.filter(\
                c_id=post_data['customer_id'])
            old_customer.update(
                c_phone = post_data['customer_phone'], \
                c_address = post_data['customer_address'])
            target_customer=old_customer[0]
        except (ObjectDoesNotExist, IndexError):
            new_customer = models.Customer.objects.create(\
                c_id=post_data['customer_id'], 
                c_name=post_data['customer_name'], 
                c_phone=post_data['customer_phone'], 
                c_address=post_data['customer_address'])
            target_customer=new_customer


        new_order = models.Order.objects.create(
            o_date=post_data['order_date'],
            o_status='Booking',
            customer=target_customer)
        
        #booking['room_name:yyyy-mm-dd:yyyy-mm-dd']
        booking_list = post_data.getlist('booking[]')
        for str_room_from_to in booking_list:
            unit = BookingUnit(str_room_from_to)
            
            try:
                sel_room = models.Room.objects.filter(r_name=unit.room_name)[0]
            except (ObjectDoesNotExist, IndexError):
                raise Http404("room does not exist")
                
            every_night = unit.every_night()
            for night_datetime in every_night:
                models.BookingRoom.objects.create(\
                    over_night_date=night_datetime,\
                    order=new_order, \
                    room=sel_room)
    
    return HttpResponse(target_customer.c_name + 'is a customer<br />query any thing');
    #else:
    #    raise Http404("data does not exist")

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