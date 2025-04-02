from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class VersionCheckJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth = super().authenticate(request)
        if auth:
            user, token = auth
            if token.payload.get('version') != user.token_version:
                raise AuthenticationFailed('Token revoked')
        return auth
