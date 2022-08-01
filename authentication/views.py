import google_auth_oauthlib.flow
from django.http.response import HttpResponseRedirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from authentication.models import User
from .apps import scopes, build_credentials


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
    user_info_service = build('oauth2', 'v2', credentials=credentials)  # Get User Details
    user_info = user_info_service.userinfo().get().execute()
    user_info.pop("verified_email")
    user_info = user_info | userCred
    try:
        user = User.objects.get(email=user_info['email'])
    except User.DoesNotExist:
        user = User(email=user_info['email'], family_name=user_info['family_name'],
                    given_name=user_info['given_name'], picture=user_info['picture'],
                    refresh=user_info['refresh'], expiry=(user_info['expiry']),
                    locale=user_info['locale'], id=user_info['id'])
        user.save()
    return Response({"token": user_info["token"]}, status=HTTP_200_OK)


@api_view(["GET"])
def success(request):
    youtube = build('youtube', 'v3', credentials=build_credentials(request.query_params.get(
        "token"), refresh_token=User.objects.get(email=request.query_params.get("email")).refresh))
    channels_response = youtube.channels().list(part='snippet,contentDetails',
                                                mine=True).execute()
    return Response({"res": channels_response}, HTTP_200_OK)
