from django.conf.urls import url
from . import views

urlpatterns = [
    #query room
    url(r'^query_room/$', views.query_room, name='query_room'),
    #order room
    url(r'^BookingRoom/$', views.booking_room, name='booking_room'),
    #checkout
    url(r'^checkout/$', views.checkout, name='checkout'),
    #checkin
    url(r'^checkin/$', views.checkin, name='checkin'),
    #test View
    url(r'^order/(?P<pk>[0-9]+)/$', views.OrderView.as_view(), name='order'),
    #initial_models
    url(r'^initialModels/', views.initial_models, name='initial_models'), 
    url(r'^createModelsData/', views.create_models_data, name='create_models_data'), 
]