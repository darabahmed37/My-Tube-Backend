from django.db import models


class Timer(models.Model):
    total_time = models.IntegerField(default=5)
    remaining_time = models.IntegerField(default=0)
    login_time = models.DateTimeField(auto_now=True)
