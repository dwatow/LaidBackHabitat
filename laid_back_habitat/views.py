# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

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
