from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from user_activity.models import Timer, WatchTiming
from user_activity.serializer import WatchTimingSerializer


class WatchTimeRAUAPIView(RetrieveUpdateDestroyAPIView):
    queryset = WatchTiming.objects.all()
    serializer_class = WatchTimingSerializer
    lookup_field = "user"


class WatchTimeListCreateAPIView(ListCreateAPIView):
    queryset = WatchTiming.objects.all()
    serializer_class = WatchTimingSerializer
