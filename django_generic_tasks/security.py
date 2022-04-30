import cachecontrol
import google.auth.transport.requests
import requests
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from ninja.security import HttpBasicAuth, HttpBearer

NoAuth = None


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        return authenticate(request, username=username, password=password)


class GoogleOIDCAuth(HttpBearer):
    session = requests.session()
    cached_session = cachecontrol.CacheControl(session)
    request = google.auth.transport.requests.Request(session=cached_session)

    def authenticate(self, request, token):
        return id_token.verify_oauth2_token(token, self.request)
