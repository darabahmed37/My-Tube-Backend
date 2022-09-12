from django.urls import path

from user_activity.views import TimerCreate, TimerRUD, PreviousTimerRetrieve

urlpatterns = [
    path('new/', TimerCreate.as_view(), name='timer-create'),
    path('', TimerRUD.as_view(), name='timer-rud'),
    path('previous', PreviousTimerRetrieve.as_view(), name='timer-previous'),

]
