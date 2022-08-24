from datetime import datetime

from rest_framework import serializers

from user_activity.models import Timer, WatchTiming


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        exclude = ("id",)
        partial = True


class WatchTimingSerializer(serializers.ModelSerializer):
    current_timer = TimerSerializer(default=True)
    previous_timers = TimerSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WatchTiming
        fields = ("current_timer", "previous_timers", "user")

    def create(self, validated_data):
        if "current_timer" in validated_data:
            current_timer_data = validated_data.pop("current_timer")
            current_timer = Timer.objects.create(**current_timer_data)
        else:
            current_timer = Timer.objects.create()

        watch_timing = WatchTiming.objects.create(user=self.context["request"].user, current_timer=current_timer,
                                                  previous_timers=None)
        return watch_timing

    def update(self, instance: WatchTiming, validated_data):
        if instance.current_timer.date.date() < datetime.now().date():
            instance.previous_timers.add(instance.current_timer)
            instance.current_timer = Timer.objects.create()

        elif "updated_time" in self.context["request"].data and instance.current_timer.used_time < instance.current_timer.total_time:
            instance.current_timer.used_time += self.context["request"].data["updated_time"]
        instance.current_timer.save()
        return instance
