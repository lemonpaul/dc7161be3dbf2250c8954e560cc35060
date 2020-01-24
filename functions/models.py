import datetime

from math import *

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core import validators

class Function(models.Model):
    formula = models.CharField(max_length=200, verbose_name="Функция")
    interval = models.IntegerField(default=0, validators=[validators.MinValueValidator(1, message="Интервал должен натуральным числом.")], verbose_name="Интервал (дни)")
    step = models.IntegerField(default=0, validators=[validators.MinValueValidator(1, message="Шаг должен быть натуральным числом.")], verbose_name="Шаг (часы)")
    modified = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return "/functions/"

    def plot(self):
        start = self.modified - datetime.timedelta(days=self.interval)
        finish = self.modified
        data = list()
        while start <= finish:
            mark = round(start.timestamp())
            t = mark
            value = eval(self.formula)
            data.append([mark, value])
            start += datetime.timedelta(hours=self.step)
        return data

    def marks(self):
        start = self.modified - datetime.timedelta(days=self.interval)
        finish = self.modified
        marks = list()
        while start <= finish:
            mark = round(start.timestamp())
            marks.append(mark)
            start += datetime.timedelta(hours=self.step)
        return marks

    def values(self):
        start = self.modified - datetime.timedelta(days=self.interval)
        finish = self.modified
        values = list()
        while start <= finish:
            t = round(start.timestamp())
            value = eval(self.formula)
            values.append(value)
            start += datetime.timedelta(hours=self.step)
        return values 

