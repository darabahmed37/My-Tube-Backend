import google_auth_oauthlib.flow
from django.http.response import HttpResponseRedirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .models import User
from .serializer import UserSerializer

scopes = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]


def get_url(flow, **kwargs):
    authorization_url, state = flow.authorization_url(access_type='offline',
                                                      include_granted_scopes='true',
                                                      **kwargs)
    return authorization_url, state


@api_view(['GET'])
def get_authentication_flow(request: Request):
    prompt = request.query_params.get("prompt", default="")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
                                                                   scopes=scopes)
    flow.redirect_uri = 'http://localhost:8000/auth/oauth2callback'
    authorization_url = "http://localhost:8000/auth/oauth2callback/error"
    if prompt == "":
        authorization_url, _ = get_url(flow)
    elif prompt == 'consent':
        authorization_url, _ = get_url(flow, prompt="consent")

    return HttpResponseRedirect(authorization_url)


@api_view(["GET"])
def oauth_callback(request):
    parms = request.query_params.dict()
    state = parms['state']
    code = parms['code']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
                                                                   scopes=scopes,
                                                                   state=state)

    flow.redirect_uri = 'http://localhost:8000/auth/oauth2callback'
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials: Credentials = flow.credentials
    userCred = {'expiry': credentials.expiry, 'token': credentials.token,
                "refresh": credentials.refresh_token}
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    user_info.pop("verified_email")
    try:
        user = User.objects.get(email=user_info['email'])
    except User.DoesNotExist:
        user = User.objects.create_user(email=user_info['email'])

        user.save()

    return Response(UserSerializer(user).data, status=HTTP_200_OK)


@api_view(["GET"])
def success(request):
    return Response({"success": True}, status=HTTP_200_OK)
