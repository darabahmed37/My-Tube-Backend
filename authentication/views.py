import google_auth_oauthlib.flow
from django.http.response import HttpResponseRedirect
from google.oauth2.credentials import Credentials
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def get_url(flow, **kwargs):
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true', **kwargs
    )
    return authorization_url, state


@api_view(['GET'])
def get_authentication_flow(request: Request):
    prompt = request.query_params.get("prompt", default="")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],

    )
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

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
        state=state
    )

    flow.redirect_uri = 'http://localhost:8000/auth/oauth2callback'
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials: Credentials = flow.credentials
    userCred = {
        'expiry': credentials.expiry,
        'token': credentials.token,
        "refresh": credentials.refresh_token
    }
    return Response(userCred)


@api_view(["GET"])
def success(request):
    return Response({"success": True}, status=HTTP_200_OK)
