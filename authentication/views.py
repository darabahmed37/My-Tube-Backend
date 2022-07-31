import google_auth_oauthlib.flow
from django.http.response import HttpResponseRedirect
from rest_framework.decorators import api_view

from authentication.models import User


@api_view(['GET'])
def get_authentication_flow(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],

    )

    flow.redirect_uri = 'http://localhost:8000/auth/oauth2callback'

    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true'
    )
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

    flow.redirect_uri = 'http://localhost:8000/auth/success'
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    user = User.objects.get(email=credentials.id_token['email'])
    return HttpResponseRedirect(flow.redirect_uri)


@api_view(["GET"])
def success(request):
    return HttpResponseRedirect('/')
