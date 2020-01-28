import datetime

from math import *

from celery import shared_task

from .models import Function


@shared_task
def generate_data(function_id):
    function = Function.objects.get(pk=function_id)
    start = function.modified - datetime.timedelta(days=function.interval)
    finish = function.modified
    marks = list()
    values = list()
    try:
        while start <= finish:
            t = round(start.timestamp())
            f = eval(function.formula)
            marks.append(t)
            values.append(f)
            start += datetime.timedelta(hours=function.step)
        function.marks = marks
        function.values = values
    except NameError as name_error:
        function.error = name_error
    except ValueError as value_error:
        function.error = value_error
    function.save()
    return
