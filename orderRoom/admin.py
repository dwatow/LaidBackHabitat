from django.contrib import admin

# Register your models here.
from models import Customer, Employee, Cleaner, Order, Payment, Service, RoomType, Room, CleanInfo, RoomsOfOrder

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('c_id', 'c_name', 'c_phone', 'c_address')

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('id', 'e_name', 'e_phone', 'e_address')

class CleanerAdmin(admin.ModelAdmin):
	list_display = ('id', 'cl_name', 'cl_phone', 'cl_address')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'o_date', 'customer', 'employee')

class PaymentAdmin(admin.ModelAdmin):
	list_display = ('id', 'p_money', 'p_account', 'p_date', 'order')

class ServiceAdmin(admin.ModelAdmin):
	list_display = ('id', 's_bike', 's_breakfast', 's_gym', 'order')

class RoomsOfOrderAdmin(admin.ModelAdmin):
	list_display = ('order', 'room', 'estimate_checkin_date', 'estimate_checkout_date')

class RoomTypeAdmin(admin.ModelAdmin):
	list_display = ('rt_name', 'rt_money')

class RoomAdmin(admin.ModelAdmin):
	list_display = ('r_name', 'room_type')

class CleanInfoAdmin(admin.ModelAdmin):
	list_display = ('id', 'cl_date', 'cleaner', 'room')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Cleaner, CleanerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(RoomsOfOrder, RoomsOfOrderAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(CleanInfo, CleanInfoAdmin)