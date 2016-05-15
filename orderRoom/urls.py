from django.conf.urls import url
from views import index
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
#    url(r'^$', index),
]