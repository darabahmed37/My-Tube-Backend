from datetime import datetime

from rest_framework import serializers

from user_activity.models import Timer, PreviousTimers


class TimerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Timer
        fields = ('total_time', 'date', 'user', "availed_time")

    def update(self, instance: Timer, validated_data):
        delta = instance.date.date() - datetime.now().date()
        if delta.days < 0:
            PreviousTimers.objects.create(total_time=instance.total_time, date=instance.date, user=instance.user, availed_time=instance.availed_time)
            instance.total_time = 2
            instance.date = datetime.now()
            instance.availed_time = False
            instance.save()
            return instance
        else:
            if instance.total_time <= 0:
                if validated_data["availed_time"] and not instance.availed_time:
                    instance.total_time = 2
                    instance.availed_time = True
                    instance.save()

                return instance
            if validated_data.get("total_time"):
                instance.total_time = validated_data['total_time']

            instance.date = datetime.now()
            instance.save()
            return instance

    def create(self, validated_data):
        return Timer.objects.create(**validated_data, user=self.context['request'].user)


class PreviousTimersSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PreviousTimers
        fields = ('total_time', 'date', 'user')
