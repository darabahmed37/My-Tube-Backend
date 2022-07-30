import google_auth_oauthlib.flow
from django.http.response import HttpResponseRedirect
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_authentication_flow(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

    flow.redirect_uri = 'http://localhost/oauth2callback'

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    return HttpResponseRedirect(authorization_url)


@api_view(["GET"])
def oauth_callback(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

    flow.redirect_uri = 'http://localhost:8000/oauth2callback'
    flow.fetch_token(authorization_response=request.get_full_path())
    credentials = flow.credentials
    return HttpResponseRedirect('/success')
