# -*- coding: utf-8 -*-
import urllib
import urllib2
import requests
import json

import pickledb
import chromelogger as console
from jsonview.decorators import json_view
from django.http import HttpResponse
from annoying.decorators import render_to


StationsCache = pickledb.load('stations.db', False)


ACC_HEADERS = {'Access-Control-Allow-Origin': '*', 
               'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
               'Access-Control-Max-Age': 1000,
               'Access-Control-Allow-Headers': '*'}
 
def cross_domain_ajax(func):
    """ Sets Access Control request headers."""
    def wrap(request, *args, **kwargs):
        # Firefox sends 'OPTIONS' request for cross-domain javascript call.
        if request.method != "OPTIONS": 
            response = func(request, *args, **kwargs)
        else:
            response = HttpResponse()
        for k, v in ACC_HEADERS.iteritems():
            response[k] = v
        return response
    return wrap


@cross_domain_ajax
@json_view
def suggester(request):
    """Принимает начало названия станции. Смотрит в кэше по первым двум буквам
    список возможных станций, если нету то спрашивает у РЖД и кэширует его.
    Далее оставляет только станции совпадающие и по остальным представленным буквам
    и возвращает их имя и id

    """
    suggest = []
    stationNamePart = request.GET.get('term','')
    firstTwoLetters = stationNamePart[:2]
    if StationsCache.get(firstTwoLetters):
        r = StationsCache.get(firstTwoLetters)
    else:
        url = 'http://pass.rzd.ru/suggester/?lang=ru&stationNamePart=%s' % firstTwoLetters
        r = requests.get(url).json()
        StationsCache.set(firstTwoLetters, r)
        StationsCache.dump()
    for st in r:
        if st['name'].lower().startswith(stationNamePart.lower()):
            suggest.append({"label": st['name'], 'value': st['id']})
    return suggest

@render_to('trains.html')
def trains(request):
    console.log(request)
    return {'rq': request.POST.items()}