from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["refresh"]
        extra_kwargs = {'password': {'write_only': True}}
