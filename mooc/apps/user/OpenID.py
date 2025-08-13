from datetime import datetime, timedelta
from os import error
from django.conf import settings
import requests
from authlib.integrations.requests_client import OAuth2Session
from authlib.common.security import generate_token
from authlib.oidc.core import CodeIDToken
from authlib.jose import jwt
import urllib


class OpenId:

    def __init__(self, client):
        
        self.client = client
        self._cache_conf = None
        self._cache_jwks = None
        
        self.session = OAuth2Session(
            settings.AUTHLIB_OAUTH_CLIENTS[client]['client_id'],
            settings.AUTHLIB_OAUTH_CLIENTS[client]['client_secret'],
            scope=settings.AUTHLIB_OAUTH_CLIENTS[client]['scope'],
        )

    @property
    def conf(self):
        # cache
        # FIXME: cache timeout
        if not self._cache_conf or self._cache_conf_timeout < datetime.now():
            # print("oauth2 load conf")
            self._cache_conf = requests.get(settings.AUTHLIB_OAUTH_CLIENTS[self.client]['server_metadata_url']).json()
            self._cache_conf_timeout = datetime.now() + timedelta(hours=4)

        return self._cache_conf
    
    @property
    def jwks(self):
        # cache
        # FIXME: cache timeout
        if not self._cache_jwks or self._cache_jwks_timeout < datetime.now():
            # print("oauth2 load jwks")
            self._cache_jwks = requests.get(self.conf['jwks_uri']).json()
            self._cache_jwks_timeout = datetime.now() + timedelta(hours=5)

        return self._cache_jwks

    def authorize_redirect(self, request, redirect_uri):
        authorization_response = request.build_absolute_uri()
        nonce = generate_token()
        uri, state = self.session.create_authorization_url(self.conf['authorization_endpoint'], redirect_uri=redirect_uri, nonce=nonce)
        request.session['openid.state'] = state

        return uri
    
    def authorize_access_token(self, request):

        # check state
        if request.GET.get('state') != request.session['openid.state']:
            raise error

        # fetch token access_token, refresh_tocken, id_tocken
        authorization_response = request.build_absolute_uri()
        tokens = self.session.fetch_token(self.conf['token_endpoint'], authorization_response=authorization_response)

        # valid openid
        claims = jwt.decode(tokens['id_token'], self.jwks, claims_cls=CodeIDToken)
        claims.validate()

        return claims, tokens

    def refresh_token(self, request, refresh_token):

        # recuperation des nouveaux tocken
        tokens = self.session.refresh_token(self.conf['token_endpoint'], refresh_token=refresh_token)

        # valid openid
        claims = jwt.decode(tokens['id_token'], self.jwks, claims_cls=CodeIDToken)
        claims.validate()

        return claims, tokens
    
    def logout(self, url=None):
        r = self.conf['end_session_endpoint']

        if url:
            r = r + "?post_logout_redirect_uri=" + urllib.parse.quote_plus(url)

        return r
