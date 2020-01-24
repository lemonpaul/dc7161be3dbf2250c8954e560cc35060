from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from .models import Function

def index(request):
    context = {'function_list': Function.objects.all()}
    return render(request, 'functions/index.html', context)

class FunctionCreate(generic.edit.CreateView):
    template_name = 'functions/add.html'
    model = Function
    fields = ['formula', 'interval', 'step']

def update(request):
    if request.method == "GET":
        for function in Function.objects.all():
            if "formula%s" % function.id in request.GET:
                function.modified = timezone.now()
                function.save()
    return HttpResponseRedirect(reverse('functions:index'))

