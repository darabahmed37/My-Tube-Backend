from rest_framework import serializers

from authentication.models import User
from user_activity.serializer import TimerSerializer


class UserSerializer(serializers.ModelSerializer):
    timer = TimerSerializer(many=False)

    class Meta:
        model = User
        exclude=["refresh"]
        extra_kwargs = {'password': {'write_only': True}}
