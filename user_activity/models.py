from django.db import models


class Timer(models.Model):
    total_time = models.IntegerField(default=5)
    remaining_time = models.IntegerField(default=0)
    login_time = models.DateTimeField(auto_now=True)
    timer = models.ForeignKey("Timer", on_delete=models.CASCADE, related_name="CurrentTimer")
    old_timers = models.ManyToManyField("Timer", related_name="PreviousTimers")
