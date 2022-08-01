import google.oauth2.credentials
import google_auth_oauthlib.flow
from django.apps import AppConfig

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
