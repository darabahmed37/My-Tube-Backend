from django.urls import path

from authentication.views import get_authentication_flow, oauth_callback

urlpatterns = [
    path('login-with-google/', get_authentication_flow, name='login'),
    path('oauth2callback/', oauth_callback, name='oauth2callback'),
]
