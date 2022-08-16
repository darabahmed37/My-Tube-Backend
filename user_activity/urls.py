from django.urls import path

from user_activity.views import TimerRAUAPIView

urlpatterns = [
    path("", TimerRAUAPIView.as_view(), name="timer"),
]
