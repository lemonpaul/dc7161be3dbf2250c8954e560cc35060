from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Function
from .tasks import generate_data


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
            task = generate_data.delay(function.id)
            task.wait()
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
                    task = generate_data.delay(function.id)
                    task.wait()
        if request.GET['action'] == 'delete':
            for function in Function.objects.all():
                if "formula%s" % function.id in request.GET:
                    function.delete()
    return HttpResponseRedirect(reverse('functions:index'))
