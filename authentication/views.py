import os
from urllib.parse import urljoin

import google_auth_oauthlib.flow
from django.contrib.auth import user_logged_in
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from authentication.apps import get_authorization_url
from authentication.apps import scopes
from authentication.models import User
from authentication.tokens import sendTokens, get_tokens_for_user

"""
This API VIEW will handle the user authentication if user want to get an refresh token then pass prompt='consent' 
in the url params. after generating the url, user will be redirected to the url where all the authentication is done
"""


class GoogleSignIn(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        prompt = request.query_params.get("prompt", default="")
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
                                                                       scopes=scopes)
        flow.redirect_uri = urljoin(os.getenv("FRONT_END_DOMAIN"), os.getenv("OAUTH_CALLBACK"))

        authorization_url = ""
        if prompt == "":
            authorization_url, _ = get_authorization_url(flow)
        elif prompt == 'consent':
            authorization_url, _ = get_authorization_url(flow, prompt="consent")
        return Response({'authorization_url': authorization_url})


"""It handle the callback by Google and Generate Google Credentials And Stores it in Database Against User"""


class OAuthCallBack(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        state = request.data.get("state")
        code = request.data.get("code")
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
                                                                       scopes=scopes,
                                                                       state=state)

        flow.redirect_uri = urljoin(os.getenv("FRONT_END_DOMAIN"), os.getenv("OAUTH_CALLBACK"))
        print(flow.redirect_uri)
        flow.fetch_token(code=code)
        credentials: Credentials = flow.credentials
        user_info_service = build('oauth2', 'v2', credentials=credentials)  # Get User Details
        user_info = user_info_service.userinfo().get().execute()
        user_info = {key: value for key, value in user_info.items() if
                     key in ["email", "family_name", "given_name", "refresh", 'id', 'locale', 'picture']}
        try:
            user = User.objects.get(email=user_info['email'])
            if credentials.refresh_token is not None:

                user.refresh = credentials.refresh_token
                user.save()
            elif user.refresh == "":

                return Response(
                    {"Message": "Error With Google Authentication",
                     "redirectUrl": urljoin(os.getenv("DOMAIN"), "auth/login-with-google/?prompt=consent")},

                    status=HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            user = User(**user_info)
            user.save()
        user_logged_in.send(sender=user.__class__,
                            request=request, user=user)
        return sendTokens(get_tokens_for_user(user))


class SignUpEmailAndPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            raise PermissionDenied("User already exists")
        except User.DoesNotExist:
            user = User.objects.create_user(email=email, password=password)
            user.save()

        return Response({"message": "User created successfully"}, status=201)


class SignInWithEmailAndPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user.refresh is None or user.refresh == "":
                    return Response(
                        {"google_uri": urljoin(os.getenv("DOMAIN"), "auth/login-with-google/?prompt=consent")})
                return Response(get_tokens_for_user(user))
            else:
                raise PermissionDenied("Invalid password")
        except User.DoesNotExist:
            raise PermissionDenied("User does not exist")


class UpdatePassword(APIView):
    def post(self, request):
        user: User = request.user
        update_parm = request.data.dict()
        if "password" in update_parm.keys():
            user.set_password(update_parm["password"])
            user.save()
            return Response({"message": "Password updated successfully"}, status=200)
        return Response({"message": "Password not updated"}, status=400)
