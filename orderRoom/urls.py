from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<link_value>[0-9]+)/$', views.test, name='test0'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test/testGet/$', views.testGet, name='testGet'),
    #order room
    url(r'^booking_room/$', views.booking_room, name='booking_room'),
    #checkout
    url(r'^checkout/$', views.checkout, name='checkout'),
    #checkin
    url(r'^checkin/$', views.checkin, name='checkin'),
]