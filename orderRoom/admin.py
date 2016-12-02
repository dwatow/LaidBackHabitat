from django.contrib import admin

# Register your models here.
from . import models

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('c_id', 'c_name', 'c_phone', 'c_address')

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('id', 'e_name', 'e_phone', 'e_address')

class CleanerAdmin(admin.ModelAdmin):
	list_display = ('id', 'cl_name', 'cl_phone', 'cl_address')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'o_status', 'o_date', 'customer', 'employee')
	date_hierarchy = 'o_date'

class PaymentAdmin(admin.ModelAdmin):
	list_display = ('id', 'p_money', 'p_account', 'p_date', 'order')
	date_hierarchy = 'p_date'

class ServiceAdmin(admin.ModelAdmin):
	list_display = ('id', 's_bike', 's_breakfast', 's_gym', 'order')

class BookingRoomAdmin(admin.ModelAdmin):
	list_display = ('order', 'room', 'over_night_date')
	date_hierarchy = 'over_night_date'

class RoomTypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'rt_name', 'rt_money')

class RoomAdmin(admin.ModelAdmin):
	list_display = ('r_name', 'room_type')

class CleanInfoAdmin(admin.ModelAdmin):
	list_display = ('id', 'cl_date', 'cleaner', 'room')
	date_hierarchy = 'cl_date'
	fields = ('cleaner', 'room')


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Cleaner, CleanerAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.BookingRoom, BookingRoomAdmin)
admin.site.register(models.RoomType, RoomTypeAdmin)
admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.CleanInfo, CleanInfoAdmin)
