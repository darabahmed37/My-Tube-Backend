from rest_framework.generics import RetrieveUpdateAPIView
from user_activity.serializer import TimerSerializer

from user_activity.models import Timer


class TimerRAUAPIView(RetrieveUpdateAPIView):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer
    lookup_field = 'user__id'
