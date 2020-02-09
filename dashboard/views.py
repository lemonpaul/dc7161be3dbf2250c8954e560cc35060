from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils import timezone

from .models import Function
from .tasks import generate_data


def index(request):
    context = {'function_list': Function.objects.all()}
    return render(request, 'dashboard/index.html', context)


def add(request):
    context = {'interval_error': False, 'step_error': False}
    if request.method == "POST":
        formula_value = str(request.POST['formula'])
        try:
            interval_value = int(request.POST['interval'])
            if interval_value < 1:
                context['interval_error'] = True
        except ValueError:
            context['interval_error'] = True
        try:
            step_value = int(request.POST['step'])
            if step_value < 1:
                context['step_error'] = True
        except ValueError:
            context['step_error'] = True
        if context['interval_error'] or context['step_error']:
            print(context)
            return render(request, 'dashboard/_add.html', context, status=202)
        else:
            function = Function.objects.create(formula=formula_value, interval=interval_value, step=step_value)
            function.save()
            task = generate_data.delay(function.id)
            task.wait()
            context = {'function_list': Function.objects.all()}
            return render(request, 'dashboard/_list.html', context)
    raise PermissionDenied


def done(request):
    if request.method == "POST":
        if request.POST['action'] == 'update':
            for function in Function.objects.all():
                if "formula%s" % function.id in request.POST:
                    function.modified = timezone.now()
                    function.save()
                    task = generate_data.delay(function.id)
                    task.wait()
        if request.POST['action'] == 'delete':
            for function in Function.objects.all():
                if "formula%s" % function.id in request.POST:
                    function.delete()
        context = {'function_list': Function.objects.all()}
        return render(request, 'dashboard/_list.html', context)
    raise PermissionDenied
