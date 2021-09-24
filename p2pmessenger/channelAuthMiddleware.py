from django.db import close_old_connections
from django.http.response import HttpResponseForbidden, HttpResponseServerError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, AuthenticationFailed
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
from channels.auth import AuthMiddlewareStack

@sync_to_async
def get_user(decoded_data):
    return get_user_model().objects.get(id=decoded_data["user_id"])
class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner
    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)



class TokenAuthMiddlewareInstance:
    """
    Custom token auth middleware
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = scope
        self.inner = self.middleware.inner
 
    async def __call__(self, receive, send):
     
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        try:
            # Get the token
            token = parse_qs(self.scope['query_string'].decode("utf8")).get("token")
            if token:
                token = token[0]
            else:
                raise AuthenticationFailed("token not provided")

    
            # Try to authenticate the user
            try:
                # This will automatically validate the token and raise an error if token is invalid
                AccessToken(token)
            except (InvalidToken, TokenError) as e:
                raise AuthenticationFailed(e)
            else:
                #  Then token is valid, decode it
                decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                # print(decoded_data)
                # Will return a dictionary like -
                # {
                #     "token_type": "access",
                #     "exp": 1568770772,
                #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
                #     "user_id": 6
                # }
    
                # Get the user using ID
                self.scope['user'] = await get_user(decoded_data)
        except AuthenticationFailed as e:
            print(e)
            return HttpResponseForbidden()
        finally:
            # Return the inner application directly and let it run everything else
            return await self.inner(self.scope, receive, send)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
