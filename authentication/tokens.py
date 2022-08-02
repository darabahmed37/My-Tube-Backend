import os

import requests
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User


def gen_tokens(email, password):
    return requests.post(os.getenv("DOMAIN") + "auth/token/", data={"email": email, "password": password}).json()


def sendTokens(response: Response, tokens):
    access, refresh = tokens["access"], tokens["refresh"]
    response.set_cookie(key='refresh_token', value=refresh, httponly=True)
    response.data = {
        'access_token': access,
    }
    return response


def get_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
