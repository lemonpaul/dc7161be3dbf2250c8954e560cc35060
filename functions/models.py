from django.db import models
from django.contrib.postgres.fields import ArrayField


class Function(models.Model):
    formula = models.CharField(max_length=200)
    interval = models.IntegerField(default=0)
    step = models.IntegerField(default=0)
    modified = models.DateTimeField(auto_now_add=True)
    marks = ArrayField(models.IntegerField(), null=True, blank=True)
    values = ArrayField(models.FloatField(), null=True, blank=True)
    error = models.CharField(max_length=200, null=True, blank=True)

    def get_absolute_url(self):
        return "/functions/"

    def format_modified(self):
        return self.modified.strftime("%Y-%m-%d %H:%M:%S.%f")

