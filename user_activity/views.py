from rest_framework.generics import RetrieveUpdateAPIView

from user_activity.models import Timer
from user_activity.serializer import TimerSerializer


class TimerRAUAPIView(RetrieveUpdateAPIView):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer
    lookup_field = ["user__email", "user__id"]
