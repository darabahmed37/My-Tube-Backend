from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import GoogleSign, oauth_callback, SignUpEmailAndPassword, \
    SignInWithEmailAndPassword, UpdatePassword

urlpatterns = [
    path('login-with-google/', GoogleSign.as_view(), name='login'),
    path('oauth2callback/', oauth_callback, name='oauth2callback'),
    path('sign-up/', SignUpEmailAndPassword.as_view(), name='sign_up_with_email_and_password'),
    path('sign-in/', SignInWithEmailAndPassword.as_view(), name='sign_in_with_email_and_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update_password/', UpdatePassword.as_view(), name='password_update'),

]
