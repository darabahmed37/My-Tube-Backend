from rest_framework import generics
from rest_framework.generics import get_object_or_404

from user_activity.models import Timer, PreviousTimers
from user_activity.serializer import TimerSerializer, PreviousTimersSerializer


class TimerCreate(generics.CreateAPIView):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer


class TimerRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TimerSerializer

    def get_object(self):
        query = Timer.objects.all()
        obj: Timer = get_object_or_404(query, user=self.request.user)
        TimerSerializer().update(obj, {})
        return obj


class PreviousTimerRetrieve(generics.ListAPIView):
    serializer_class = PreviousTimersSerializer

    def get_queryset(self):
        return PreviousTimers.objects.filter(user=self.request.user.email).order_by("date")
