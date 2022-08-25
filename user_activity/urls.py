from django.urls import path

from user_activity.views import TimerCreate, TimerRUD, PreviousTimerRetrieve

urlpatterns = [
    path('', TimerCreate.as_view(), name='timer-create'),
    path('<str:user>/', TimerRUD.as_view(), name='timer-rud'),
    path('previous/<str:user>/', PreviousTimerRetrieve.as_view(), name='timer-rud'),

]
