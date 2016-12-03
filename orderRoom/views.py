# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_list_or_404
from . import models
from .MyLib.MyDateTime import MyDateTime
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from . import forms
import os
import datetime

class EmptyRoomTypeHistogram:
    def __total_room_num(self):
        target_room_type = models.RoomType.objects.filter(rt_name=self.room_type_name)
        return len(models.Room.objects.filter(room_type=target_room_type))

    def __curr_booking_room_list(self):
        target_room_type = models.RoomType.objects.get(rt_name=self.room_type_name)
        target_rooms = models.Room.objects.filter(room_type=target_room_type)
        from_datetime = self.from_date.date_time()
        to_datetime = self.to_date.date_time()
        return models.BookingRoom.objects.filter(room=target_rooms, over_night_date__range=(self.from_date.date_time(), self.to_date.date_time()))

    def __init__(self, room_type, str_from_date='', str_to_date=''):
        self.limit_days = 100
        if str_from_date and not str_to_date:
            self.room_type_id = room_type.id
            self.room_type_name = room_type.rt_name
            self.from_date = MyDateTime(str_from_date)
            self.to_date = MyDateTime(str_from_date)

            self.histogram = 0
            self.histogram = self.__total_room_num()

            for curr_booking in self.__curr_booking_room_list():
                self.histogram -= 1
                if self.histogram < 0:
                    self.histogram = 0

        elif str_from_date and str_to_date:
            self.room_type_id = room_type.id
            self.room_type_name = room_type.rt_name
            self.from_date = MyDateTime(str_from_date)
            self.to_date = MyDateTime(str_to_date)

            self.curr_range_days = abs(self.from_date.comprise_between(self.to_date))
            if self.curr_range_days > self.limit_days:
                return
            #initial
            range_days = self.from_date.comprise_everyday(self.to_date)

            self.histogram = {}
            for everyday in range_days:
                self.histogram[everyday.year] = {}

            for everyday in range_days:
                self.histogram[everyday.year][everyday.month] = {}

            for everyday in range_days:
                self.histogram[everyday.year][everyday.month][everyday.day] = self.__total_room_num()

            #set value
            for curr_booking in self.__curr_booking_room_list():
                year  = curr_booking.over_night_date.year
                month = curr_booking.over_night_date.month
                day   = curr_booking.over_night_date.day

                if year in self.histogram and month in self.histogram[year] and day in self.histogram[year][month]:
                    self.histogram[year][month][day] -= 1
                    if self.histogram[year][month][day] < 0:
                       self.histogram[year][month][day] = 0
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
    today_date = request.GET.get('today', '')
    from_date = request.GET.get('from', '')
    to_date = request.GET.get('to', '')

    if today_date:
        histogram=[]
        for room_type in list(models.RoomType.objects.all()):
            histogram_unit = EmptyRoomTypeHistogram(room_type, today_date)
            histogram.append(histogram_unit)

        return render_to_response('BookingList1.html', locals())
    elif from_date and to_date:
        histogram = []
        for room_type in list(models.RoomType.objects.all()):
            histogram_unit = EmptyRoomTypeHistogram(room_type, from_date, to_date)
            histogram.append(histogram_unit)
        # EmptyRoomTyppHistogram(models.RoomType.objects.all()[0], from_date, to_date)
        return render_to_response('BookingList2.html', locals())
    else:
        return render_to_response('BookingList1.html', locals())


def booking_room(request):
    get_data = request.GET
    default_datetime = ''
    default_room_type_id = ''
    if get_data:
        default_datetime = get_data.get('booking_datetime', '')
        default_room_type_id = get_data.get('booking_room_type_id', '')

    post_data = request.GET
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
            #sel_room = get_object_or_404(Room, r_name=unit.room_name)
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


    booking_room_form = forms.OrderForm()
    room_type_list = models.RoomType.objects.all();
    return render_to_response('BookingRoom.html',locals())
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

def login(request):
    return HttpResponseRedirect('/accounts/login/')

def logout(request):
    return HttpResponseRedirect('/accounts/logout/')




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

class OrderView(generic.DetailView):
    model = models.Order
    #template_name = 'order_detail.html'
    #template_name = 'order_list.html'


def initial_models(request):
    os.system('initial_models.bat')
    return HttpResponse('')

def create_models_data(request):
    if not models.Customer.objects.filter(c_id='X173918116'):
        models.Customer.objects.create(c_id='X173918116', c_name='林伯彥', c_phone='0923415233', c_address='臺灣府城三界壇街')
    if not models.Customer.objects.filter(c_id='X163416802'):
        models.Customer.objects.create(c_id='X163416802', c_name='陳仙鶴', c_phone='0933958463', c_address='府城銀同里')
    if not models.Customer.objects.filter(c_id='X163416801'):
        models.Customer.objects.create(c_id='X163416801', c_name='陳復甫', c_phone='0933958463', c_address='明朝福建路漳州府龍溪')
    if not models.Customer.objects.filter(c_id='X160016836'):
        models.Customer.objects.create(c_id='X160016836', c_name='馮希範', c_phone='0939028276', c_address='泉州晉江縣')
    if not models.Customer.objects.filter(c_id='X123654263'):
        models.Customer.objects.create(c_id='X123654263', c_name='鄭賢之', c_phone='0987654322', c_address='大明泉州府南安縣')
    if not models.Customer.objects.filter(c_id='X123456789'):
        models.Customer.objects.create(c_id='X123456789', c_name='唐維卿', c_phone='0934564535', c_address='臺灣民主國臺南大天后宮')

    if not models.Employee.objects.filter(e_name='test employee'):
        models.Employee.objects.create(e_name='test employee', e_phone='123435', e_address='test employee addr')

    if not models.Cleaner.objects.filter(cl_name='test cleaner'):
        models.Cleaner.objects.create(cl_name='test cleaner', cl_phone='123456', cl_address='test cleaner addr')

    if not models.RoomType.objects.filter(rt_name='雙人和式套房'):
        models.RoomType.objects.create(rt_name='雙人和式套房', rt_money='3600')
    if not models.RoomType.objects.filter(rt_name='日式通鋪四人'):
        models.RoomType.objects.create(rt_name='日式通鋪四人', rt_money='3400')
    if not models.RoomType.objects.filter(rt_name='日式通鋪六人'):
        models.RoomType.objects.create(rt_name='日式通鋪六人', rt_money='5100')
    if not models.RoomType.objects.filter(rt_name='日式通鋪八人'):
        models.RoomType.objects.create(rt_name='日式通鋪八人', rt_money='6800')
    if not models.RoomType.objects.filter(rt_name='四人和式套房'):
        models.RoomType.objects.create(rt_name='四人和式套房', rt_money='6000')

    if not models.Room.objects.filter(r_name='room 9'):
        models.Room.objects.create(r_name='room 9', room_type=models.RoomType.objects.get(rt_name='雙人和式套房'))
    if not models.Room.objects.filter(r_name='room 8'):
        models.Room.objects.create(r_name='room 8', room_type=models.RoomType.objects.get(rt_name='雙人和式套房'))
    if not models.Room.objects.filter(r_name='room 7'):
        models.Room.objects.create(r_name='room 7', room_type=models.RoomType.objects.get(rt_name='雙人和式套房'))
    if not models.Room.objects.filter(r_name='room 6'):
        models.Room.objects.create(r_name='room 6', room_type=models.RoomType.objects.get(rt_name='四人和式套房'))
    if not models.Room.objects.filter(r_name='room 5'):
        models.Room.objects.create(r_name='room 5', room_type=models.RoomType.objects.get(rt_name='四人和式套房'))
    if not models.Room.objects.filter(r_name='room 4'):
        models.Room.objects.create(r_name='room 4', room_type=models.RoomType.objects.get(rt_name='日式通鋪四人'))
    if not models.Room.objects.filter(r_name='room 3'):
        models.Room.objects.create(r_name='room 3', room_type=models.RoomType.objects.get(rt_name='日式通鋪四人'))
    if not models.Room.objects.filter(r_name='room 2'):
        models.Room.objects.create(r_name='room 2', room_type=models.RoomType.objects.get(rt_name='日式通鋪六人'))
    if not models.Room.objects.filter(r_name='room 10'):
        models.Room.objects.create(r_name='room 10', room_type=models.RoomType.objects.get(rt_name='雙人和式套房'))
    if not models.Room.objects.filter(r_name='room 1'):
        models.Room.objects.create(r_name='room 1', room_type=models.RoomType.objects.get(rt_name='日式通鋪八人'))

    if not models.Order.objects.filter(o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X163416801')):
        models.Order.objects.create(o_status='Booking', o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X163416801'))
    if not models.Order.objects.filter(o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X123654263')):
        models.Order.objects.create(o_status='Booking', o_date=datetime.datetime(2016, 5, 21), customer=models.Customer.objects.get(c_id='X123654263'))
    if not models.Order.objects.filter(o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X163416802')):
        models.Order.objects.create(o_status='Booking', o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X163416802'))
    if not models.Order.objects.filter(o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X173918116')):
        models.Order.objects.create(o_status='Booking', o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X173918116'))

    order1 = models.Order.objects.get(o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X163416802'))
    room4 = models.Room.objects.get(r_name='room 4')
    if not models.BookingRoom.objects.filter(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 9)):
        models.BookingRoom.objects.create(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 9))
    if not models.BookingRoom.objects.filter(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 8)):
        models.BookingRoom.objects.create(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 8))
    if not models.BookingRoom.objects.filter(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 7)):
        models.BookingRoom.objects.create(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 7))
    if not models.BookingRoom.objects.filter(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 6)):
        models.BookingRoom.objects.create(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 6))
    if not models.BookingRoom.objects.filter(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 5)):
        models.BookingRoom.objects.create(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 5))
    if not models.BookingRoom.objects.filter(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 4)):
        models.BookingRoom.objects.create(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 4))
    if not models.BookingRoom.objects.filter(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 3)):
        models.BookingRoom.objects.create(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 3))
    if not models.BookingRoom.objects.filter(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 2)):
        models.BookingRoom.objects.create(order=order1, room=room4, over_night_date=datetime.datetime(2016, 6, 2))

    order2 = models.Order.objects.get(o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X173918116'))
    room3 = models.Room.objects.get(r_name='room 3')
    if not models.BookingRoom.objects.filter(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 9)):
        models.BookingRoom.objects.create(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 9))
    if not models.BookingRoom.objects.filter(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 8)):
        models.BookingRoom.objects.create(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 8))
    if not models.BookingRoom.objects.filter(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 7)):
        models.BookingRoom.objects.create(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 7))
    if not models.BookingRoom.objects.filter(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 6)):
        models.BookingRoom.objects.create(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 6))
    if not models.BookingRoom.objects.filter(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 5)):
        models.BookingRoom.objects.create(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 5))
    if not models.BookingRoom.objects.filter(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 4)):
        models.BookingRoom.objects.create(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 4))
    if not models.BookingRoom.objects.filter(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 3)):
        models.BookingRoom.objects.create(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 3))
    if not models.BookingRoom.objects.filter(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 2)):
        models.BookingRoom.objects.create(order=order2, room=room3, over_night_date=datetime.datetime(2016, 6, 2))

    if not models.Payment.objects.filter(p_money=999, p_account='12345678789', p_date=datetime.datetime(2016, 5, 16), order=models.Order.objects.get(o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X163416802'))):
        models.Payment.objects.create(p_money=999, p_account='12345678789', p_date=datetime.datetime(2016, 5, 16), order=models.Order.objects.get(o_date=datetime.datetime(2016, 5, 22), customer=models.Customer.objects.get(c_id='X163416802')))

    if not models.Service.objects.filter(s_bike='1', s_breakfast='1', s_gym='1'):
        models.Service.objects.create(s_bike='1', s_breakfast='1', s_gym='1')

    if not models.CleanInfo.objects.filter(cl_date=datetime.datetime(2016, 5, 3), cleaner=models.Cleaner.objects.get(cl_name='test cleaner'), room=models.Room.objects.get(r_name='room 3')):
        models.CleanInfo.objects.create(cl_date=datetime.datetime(2016, 5, 3), cleaner=models.Cleaner.objects.get(cl_name='test cleaner'), room=models.Room.objects.get(r_name='room 3'))

    return HttpResponse('ok')
