import datetime

from math import *

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core import validators
from django.contrib.postgres.fields import ArrayField

class Function(models.Model):
    formula = models.CharField(max_length=200)
    interval = models.IntegerField(default=0)
    step = models.IntegerField(default=0)
    modified = models.DateTimeField(auto_now_add=True)
    marks=ArrayField(models.IntegerField(), null=True, blank=True)
    values = ArrayField(models.FloatField(), null=True, blank=True)

    def get_absolute_url(self):
        return "/functions/"

    def generate_data(self):
        start = self.modified - datetime.timedelta(days=self.interval)
        finish = self.modified
        marks = list()
        values = list()
        while start <= finish:
            t = round(start.timestamp())
            f = eval(self.formula)
            marks.append(t)
            values.append(f)
            start += datetime.timedelta(hours=self.step)
        self.marks = marks
        self.values = values
        return


    def error(self):
        try:
            eval(self.formula)
            error = "formula is valid"
        except NameError as nameError:
            error = nameError
        return error

    def format_modified(self):
        return self.modified.strftime("%Y-%m-%d %H:%M:%S.%f")

