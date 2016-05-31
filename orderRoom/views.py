# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response, get_list_or_404
from . import models
from .MyLib.MyDateTime import MyDateTime
from django.core.exceptions import ObjectDoesNotExist

class EmptyRoomTypeHistogram:
    def __total_room_num(self):
        target_room_type = models.RoomType.objects.filter(rt_name=self.room_type_name)
        return len(models.Room.objects.filter(room_type=target_room_type))

    def __curr_booking_room_list(self):
        target_room_type = models.RoomType.objects.get(rt_name=self.room_type_name)
        target_rooms = models.Room.objects.filter(room_type=target_room_type)
        return models.BookingRoom.objects.filter(room=target_rooms, over_night_date__range=(self.from_date.date_time(), self.to_date.date_time()))

    def __init__(self, room_type_name, str_from_date='', str_to_date=''):
    	if str_from_date:
	        self.room_type_name = room_type_name
	        self.from_date = MyDateTime(str_from_date)
	        self.to_date = MyDateTime(str_from_date)

	        self.histogram = 0
	        self.histogram = self.__total_room_num()

	        for curr_booking in self.__curr_booking_room_list():
	            histogram -= 1
	            if histogram < 0:
	                histogram = 0

    	elif str_from_date and str_to_date:
            self.room_type_name = room_type_name
            self.from_date = MyDateTime(str_from_date)
            self.to_date = MyDateTime(str_to_date)

            #initial
            range_days = self.from_date.comprise_everyday(self.to_date)

            self.histogram = {}
            for everyday in range_days:
                self.histogram[everyday.month] = {}

            for everyday in range_days:
                self.histogram[everyday.month][everyday.day] = self.__total_room_num()

            #set value
            for curr_booking in self.__curr_booking_room_list():
                month = curr_booking.over_night_date.month
                day   = curr_booking.over_night_date.day
                self.histogram[month][day] -= 1
                if self.histogram[month][day] < 0:
                       self.histogram[month][day] = 0

class BookingUnit:
    #room:yyyy_mm_dd:yyyy_mm_dd
    def __init__(self, str_room_from_data_to_data):
        self.room_name, from_date, to_date = str_room_from_data_to_data.split(':')
        self.from_datetime = MyDateTime(from_date)
        self.to_datetime = MyDateTime(to_date)

    def total_day(self):
        return self.from_datetime.comprise_between(self.to_datetime)

    def every_night(self):
        return self.from_datetime.comprise_everyday(self.to_datetime)



# Create your views here.


def query_room(request):
    curr_date = request.GET['today']

    histogram=[]
    for room_type in list(models.RoomType.objects.all()):
        histogram_unit = EmptyRoomTypeHistogram(room_type.rt_name, curr_date)
        histogram.append(histogram_unit)

    return render_to_response('BookingList1.html', locals())

def query_room_list(request):
    get_data = request.GET;
    from_date = get_data['from']
    to_date = get_data['to']

    histogram = []
    for room_type in list(models.RoomType.objects.all()):
        histogram_unit = EmptyRoomTypeHistogram(room_type.rt_name, from_date, to_date)
        histogram.append(histogram_unit)

    return render_to_response('BookingList2.html', locals())

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