from django.urls import path

from user_activity.views import WatchTimeRAUAPIView, WatchTimeListCreateAPIView

urlpatterns = [
    path("<str:user>/", WatchTimeRAUAPIView.as_view(), name="timer-detail"),
    path("", WatchTimeListCreateAPIView.as_view()),
]
