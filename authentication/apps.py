import google.oauth2.credentials
import google_auth_oauthlib.flow

from django.apps import AppConfig
from django.http import HttpRequest
from googleapiclient.discovery import build
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request

scopes = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'


def build_credentials(token, refresh_token):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
                                                                   scopes=scopes)
    parms = {
        "token": token,
        "refresh_token": refresh_token,
        "scopes": scopes,
        "client_id": flow.client_config['client_id'],
        "client_secret": flow.client_config['client_secret'],
        "enable_reauth_refresh": True,
        "token_uri": flow.client_config['token_uri']
    }
    credentials = google.oauth2.credentials.Credentials(**parms)
    return credentials


def get_youtube(request: Request):
    if request.user.refresh is None or request.user.refresh == "":
        raise PermissionDenied("User does not have a refresh token")
    credentials = build_credentials(token=None, refresh_token=request.user.refresh_token)
    return build("youtube", 'v3', credentials=credentials)


Request = HttpRequest | Request
