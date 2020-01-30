import datetime
import urllib3
import json
import os

from math import *

from django.core.files import File
from celery import shared_task

from .models import Function


@shared_task
def generate_data(function_id):
    function = Function.objects.get(pk=function_id)
    start = function.modified - datetime.timedelta(days=function.interval)
    finish = function.modified
    try:
        t = list(range(round(start.timestamp()), round(finish.timestamp())+1, function.step * 3600))
        f = list(map(lambda t: eval(function.formula), t))
        data = {'infile': {'title': {'text': ''}, 'xAxis': {'categories': t}, 'yAxis': {'title': {'text': ''}},
                           'series': [{'showInLegend': False, 'name': 'f(t)', 'data': f}]}}
        http = urllib3.PoolManager()
        response = http.request('POST', 'http://highcharts:8080', headers={'Content-Type': 'application/json'}, body=json.dumps(data))
        open('media/images/plot.png', 'wb').write(response.data)
        if function.plot:
            if os.path.isfile(function.plot.path):
                os.remove(function.plot.path)
        function.plot.save('plot.png', File(open('media/images/plot.png', 'rb')))
        os.remove('media/images/plot.png')
    except NameError as name_error:
        function.error = name_error
    except ValueError as value_error:
        function.error = value_error
    function.save()
    return
