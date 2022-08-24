from rest_framework import serializers

from user_activity.models import Timer, WatchTiming


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        exclude = ("id",)


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

    def update_current_timer(self, watch_timing, current_timer_data):
        watch_timing.previous_timers.add(watch_timing.current_timer)
        watch_timing.current_timer = Timer.objects.create(**current_timer_data)
        watch_timing.save()
        return watch_timing

