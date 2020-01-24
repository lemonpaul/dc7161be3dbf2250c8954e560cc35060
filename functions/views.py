from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Function


def index(request):
    context = {'function_list': Function.objects.all()}
    return render(request, 'functions/index.html', context)


def add(request):
    context = {'interval_error': False, 'step_error': False}
    if request.method == "POST":
        formula_value = str(request.POST['formula'])
        interval_value = int(request.POST['interval'])
        step_value = int(request.POST['step'])
        if interval_value < 1:
            context['interval_error'] = True
        else:
            context['interval_error'] = False
        if step_value < 1:
            context['step_error'] = True
        else:
            context['step_error'] = False
        if context['interval_error'] or context['step_error']:
            return render(request, 'functions/add.html', context)
        else:
            function = Function.objects.create(formula=formula_value, interval=interval_value, step=step_value)
            function.generate_data()
            function.save()
            return HttpResponseRedirect(reverse('functions:index'))
    else:
        return render(request, 'functions/add.html', context)


def done(request):
    if request.method == "GET":
        if request.GET['action'] == 'update':
            for function in Function.objects.all():
                if "formula%s" % function.id in request.GET:
                    function.modified = timezone.now()
                    function.generate_data()
                    function.save()
    return HttpResponseRedirect(reverse('functions:index'))
