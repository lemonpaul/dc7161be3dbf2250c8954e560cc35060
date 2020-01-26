import datetime

from math import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Function


def generate_data(id):
    function = Function.objects.get(pk=id)
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
        function.save()
        return
    except NameError as name_error:
        function.error = name_error
        function.save()
        return
    except ValueError as value_error:
        function.error = value_error
        function.save()
        return


def index(request):
    context = {'function_list': Function.objects.all()}
    return render(request, 'functions/index.html', context)


def add(request):
    context = {'interval_error': False, 'step_error': False}
    if request.method == "POST":
        formula_value = str(request.POST['formula'])
        try:
            interval_value = int(request.POST['interval'])
            if interval_value < 1:
                context['interval_error'] = True
            else:
                context['interval_error'] = False
        except ValueError:
            context['interval_error'] = True
        try:
            step_value = int(request.POST['step'])
            if step_value < 1:
                context['step_error'] = True
            else:
                context['step_error'] = False
        except ValueError:
            context['step_error'] = True
        if context['interval_error'] or context['step_error']:
            return render(request, 'functions/add.html', context)
        else:
            function = Function.objects.create(formula=formula_value, interval=interval_value, step=step_value)
            function.save()
            generate_data(function.id)
            return HttpResponseRedirect(reverse('functions:index'))
    else:
        return render(request, 'functions/add.html', context)


def done(request):
    if request.method == "GET":
        if request.GET['action'] == 'update':
            for function in Function.objects.all():
                if "formula%s" % function.id in request.GET:
                    function.modified = timezone.now()
                    function.save()
                    generate_data(function.id)
        if request.GET['action'] == 'delete':
            for function in Function.objects.all():
                if "formula%s" % function.id in request.GET:
                    function.delete()
    return HttpResponseRedirect(reverse('functions:index'))
