from django.db import models


class Function(models.Model):
    formula = models.CharField(max_length=200)
    interval = models.IntegerField(default=0)
    step = models.IntegerField(default=0)
    modified = models.DateTimeField(auto_now_add=True)
    plot = models.ImageField(upload_to='images/', null=True, blank=True)
    error = models.CharField(max_length=200, null=True, blank=True)

    @staticmethod
    def get_absolute_url():
        return "/dashboard/"

    def format_modified(self):
        return self.modified.strftime("%Y-%m-%d %H:%M:%S.%f")
