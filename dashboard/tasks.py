import datetime
import urllib3
import json
import os

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

from django.core.files import File
from celery import shared_task

from .models import Function


@shared_task
def generate_data(function_id):
    func = Function.objects.get(pk=function_id)
    start = func.modified - datetime.timedelta(days=func.interval)
    finish = func.modified
    t = list(range(round(start.timestamp()), round(finish.timestamp()) + 1, func.step * 3600))
    try:
        f = list(map(lambda x: float(parse_expr(func.formula).subs({"t": float(x)})), t))
    except TypeError as error:
        func.error = error
        func.save()
        return
    data = {'infile': {'title': {'text': ''}, 'xAxis': {'categories': t}, 'yAxis': {'title': {'text': ''}},
                       'series': [{'showInLegend': False, 'name': 'f(t)', 'data': f}]}}
    http = urllib3.PoolManager()
    response = http.request('POST', 'http://highcharts:8080', headers={'Content-Type': 'application/json'},
                            body=json.dumps(data))
    if func.plot:
        os.remove(func.plot.path)
    open('plot.png', 'wb').write(response.data)
    func.plot.save('%s.png' % datetime.datetime.now().timestamp(), File(open('plot.png', 'rb')))
    os.remove('plot.png')
    func.save()
    return
