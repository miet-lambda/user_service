from drf_spectacular.extensions import OpenApiAuthenticationExtension
from users.authentication import VersionCheckJWTAuthentication

class VersionCheckJWTScheme(OpenApiAuthenticationExtension):
    target_class = VersionCheckJWTAuthentication
    name = 'JWT'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': (
                'JWT authentication with version checking. '
                'Tokens are invalidated when user revoke-tokens/'
            )
        }
