from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from authentication.views import google_sign_in, oauth_callback, sign_up_with_email_and_password, \
    sign_in_with_email_and_password, update_password

urlpatterns = [
    path('login-with-google/', google_sign_in, name='login'),
    path('oauth2callback/', oauth_callback, name='oauth2callback'),
    path('sign-up/', sign_up_with_email_and_password, name='sign_up_with_email_and_password'),
    path('sign-in/', sign_in_with_email_and_password, name='sign_in_with_email_and_password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update_password/', update_password, name='password_update')

]
