from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import GoogleSignIn, OAuthCallBack, SignUpEmailAndPassword, \
    SignInWithEmailAndPassword, UpdatePassword, GetUserInfo, DeleteUser

urlpatterns = [
    path('login-with-google/', GoogleSignIn.as_view(), name='login'),
    path('oauth2callback/', OAuthCallBack.as_view(), name='oauth2callback'),
    path('sign-up/', SignUpEmailAndPassword.as_view(), name='sign_up_with_email_and_password'),
    path('sign-in/', SignInWithEmailAndPassword.as_view(), name='sign_in_with_email_and_password'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update-password/', UpdatePassword.as_view(), name='password_update'),
    path("get-user/", GetUserInfo.as_view(), name="get_user"),
    path("delete-user/", DeleteUser.as_view(), name="delete_user"),
]
