from rest_framework import serializers

from authentication.models import User
from user_activity.models import Timer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["refresh"]
        extra_kwargs = {'password': {'write_only': True}}

