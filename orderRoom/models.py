from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Customer(models.Model):
    c_id = models.CharField(max_length=10, primary_key=True)
    c_name = models.CharField(max_length=255)
    c_phone = models.CharField(max_length=10)
    c_address = models.CharField(max_length=255, blank=False)

    def __str__(self):              # __unicode__ on Python 2
        return "Customer: %s, %s" % (self.c_id, self.c_name)

class Employee(models.Model):
    # e_id = models.IntegerField(default=0)
    e_name = models.CharField(max_length=255)
    e_phone = models.CharField(max_length=10)
    e_address = models.CharField(max_length=255, blank=False)

    def __str__(self):              # __unicode__ on Python 2
        return "Employee: %s" % (self.e_name)

class Cleaner(models.Model):
    # cl_id = models.IntegerField(default=0)
    cl_name = models.CharField(max_length=255)
    cl_phone = models.CharField(max_length=10)
    cl_address = models.CharField(max_length=255, blank=False)

    def __str__(self):              # __unicode__ on Python 2
        return "Cleaner: %s" % (self.cl_name)

class RoomType(models.Model):
    # rt_id = models. CharField(max_length=255)
    rt_name = models.CharField(max_length=255, primary_key=True)
    rt_money = models.IntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
        return "RoomType: %s, %s" % (self.rt_name, self.rt_money)

class Room (models.Model):
    # r_id = models.CharField(max_length=255)
    # r_type = models.CharField(max_length=255)

    r_name = models.CharField(max_length=255, primary_key=True)    
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    # cleaner = models.ManyToManyField(Cleaner)

    def __str__(self):              # __unicode__ on Python 2
        return "Room: %s, %s" % (self.r_name, self.room_type.rt_name)

class Order(models.Model):
    # p_id = models.IntegerField(default=0)
    o_date = models.DateTimeField()
    #c_id = models.CharField(max_length=10)
    #e_id = models.CharField(max_length=255)
    #r_id = models.CharField(max_length=255)

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=False)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=False)
    # Room = models.ForeignKey(Room)
    
    def __str__(self):              # __unicode__ on Python 2
        # return "Order: %s" % (self.o_date)
        return "Order: %s, (%s)%s, (%s)%s" % (self.o_date, self.customer.c_id, self.customer.c_name, self.employee.id, self.employee.e_name)

class RoomsOfOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    estimate_checkin_date = models.DateTimeField()
    estimate_checkout_date = models.DateTimeField()

    def __str__(self):              # __unicode__ on Python 2
        return "RoomsOfOrder: %s, %s, %s, %s" % (self.order, self.room, self.estimate_checkin_date, self.estimate_checkout_date)

class Payment(models.Model):
    # p_id = models.IntegerField(default=0)
    p_money = models.IntegerField(default=0)
    p_account = models.CharField(max_length=255)
    p_date = models.DateTimeField()

    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):              # __unicode__ on Python 2
        return "Payment: %s, %s, %s, %s" % (self.p_account, self.p_money, self.p_date, self.order)

class Service(models.Model):
    # s_id = models.IntegerField(default=0)
    s_bike = models.CharField(max_length=1)
    s_breakfast = models.CharField(max_length=1)
    s_gym = models.CharField(max_length=1)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return "Service: %s, %s, %s, %s" % (self.s_bike, self.s_breakfast, self.s_gym, self.order)

class CleanInfo(models.Model):
    # clinfo_id = models.IntegerField(default=0)
    # cl_id = models.IntegerField(default=0)
    # r_id = models.CharField(max_length=255)
    cl_date = models.DateTimeField()

    cleaner = models.ForeignKey(Cleaner, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return "CleanInfo: %s, (%s)%s, %s" % (self.cl_date, self.cleaner.id, self.cleaner.cl_name, self.room.r_name)
