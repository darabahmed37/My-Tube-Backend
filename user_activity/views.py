from rest_framework import generics

from user_activity.models import Timer, PreviousTimers
from user_activity.serializer import TimerSerializer, PreviousTimersSerializer


class TimerCreate(generics.CreateAPIView):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer


class TimerRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer
    lookup_field = "user"


class PreviousTimerRetrieve(generics.ListAPIView):
    queryset = PreviousTimers.objects.all()
    serializer_class = PreviousTimersSerializer
    lookup_field = "user"
