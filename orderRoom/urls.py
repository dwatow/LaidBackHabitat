from django.conf.urls import url
from . import views

urlpatterns = [
    #query room
    url(r'^query_room/$', views.query_room, name='query_room'),
    url(r'^query_room_list/$', views.query_room_list, name='query_room_list'),
    #order room
    url(r'^booking_room/$', views.booking_room, name='booking_room'),
    #checkout
    url(r'^checkout/$', views.checkout, name='checkout'),
    #checkin
    url(r'^checkin/$', views.checkin, name='checkin'),
    #test View
    url(r'^order/(?P<pk>[0-9]+)/$', views.OrderView.as_view(), name='order'),
]