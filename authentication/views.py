import os
from urllib.parse import urljoin

import google_auth_oauthlib.flow
from django.contrib.auth import user_logged_in
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.apps import get_authorization_url
from authentication.apps import scopes
from authentication.models import User
from authentication.tokens import sendTokens, get_tokens_for_user

"""
This API VIEW will handle the user authentication if user want to get an refresh token then pass prompt='consent' 
in the url params. after generating the url, user will be redirected to the url where all the authentication is done
"""


class GoogleSign(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        prompt = request.query_params.get("prompt", default="")
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
                                                                       scopes=scopes)
        flow.redirect_uri = urljoin(os.getenv("DOMAIN"), 'auth/oauth2callback')

        authorization_url = urljoin(os.getenv('DOMAIN'), "auth/oauth2callback/error")
        if prompt == "":
            authorization_url, _ = get_authorization_url(flow)
        elif prompt == 'consent':
            authorization_url, _ = get_authorization_url(flow, prompt="consent")
        return Response({'authorization_url': authorization_url})


@api_view(["GET"])
@permission_classes([AllowAny])
def oauth_callback(request):
    parms = request.query_params.dict()
    state = parms['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
                                                                   scopes=scopes,
                                                                   state=state)

    flow.redirect_uri = urljoin(os.getenv("DOMAIN"), 'auth/oauth2callback')
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials: Credentials = flow.credentials
    user_info_service = build('oauth2', 'v2', credentials=credentials)  # Get User Details
    user_info = user_info_service.userinfo().get().execute()
    user_info = {key: value for key, value in user_info.items() if
                 key in ["email", "family_name", "given_name", "refresh", 'id', 'locale', 'picture']}
    try:
        user = User.objects.get(email=user_info['email'])
        if user.refresh == "":
            if credentials.refresh_token is not None:
                user.refresh = credentials.refresh_token
                user.save()
            else:

                return Response({'login_url': urljoin(os.getenv("DOMAIN"), "auth/login-with-google/?prompt=consent")},
                                status=status.HTTP_307_TEMPORARY_REDIRECT)
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
