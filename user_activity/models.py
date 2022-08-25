from django.db import models


class Timer(models.Model):
    total_time = models.FloatField(default=5)
    date_time = models.DateTimeField(auto_now_add=True)


class WatchTiming(models.Model):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, primary_key=True)
    current_timer = models.ForeignKey(Timer, on_delete=models.CASCADE, related_name="current_timer")
    previous_timers = models.ForeignKey(Timer, on_delete=models.CASCADE, related_name="previous_timers")
