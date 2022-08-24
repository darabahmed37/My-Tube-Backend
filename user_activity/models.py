from django.db import models


class Timer(models.Model):
    total_time = models.FloatField(default=5)
    used_time = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=True)


class WatchTiming(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, primary_key=True)
    current_timer = models.OneToOneField(Timer, on_delete=models.CASCADE, related_name='current_timer')
    previous_timers = models.ForeignKey(Timer, on_delete=models.CASCADE, related_name="previous_timers", null=True)
