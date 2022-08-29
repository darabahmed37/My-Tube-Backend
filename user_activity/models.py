from django.db import models


class Timer(models.Model):
    total_time = models.FloatField(default=5)
    date = models.DateTimeField(auto_now=True)
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)


class PreviousTimers(models.Model):
    total_time = models.FloatField(default=5)
    date = models.DateTimeField()
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
