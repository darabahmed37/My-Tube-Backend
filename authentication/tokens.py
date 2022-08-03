import os

import requests
from django.http.response import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User


def gen_tokens(email, password):
    return requests.post(os.getenv("DOMAIN") + "auth/token/", data={"email": email, "password": password}).json()


def sendTokens(tokens):
    access, refresh = tokens["access"], tokens["refresh"]
    response = HttpResponseRedirect(redirect_to=os.getenv("FRONT_END_DOMAIN") + "success/")
    response.set_cookie(key='refresh', value=refresh, httponly=True)
    response.set_cookie(key='access', value=access, httponly=True)

    return response


def get_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
