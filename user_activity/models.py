from django.db import models


class Timer(models.Model):
    total_time = models.IntegerField()
    remaining_time = models.IntegerField()
    login_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, primary_key=True)
