from rest_framework import serializers

from .models import Timer


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        exclude = ("id",)


class WatchTimingSerializer(serializers.ModelSerializer):
    current_timer = TimerSerializer(default=Timer.objects.create())
    previous_timers = TimerSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
