from datetime import datetime, timezone
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError




class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                token = AccessToken(access_token)
                exp_time = datetime.fromtimestamp(token['exp'], timezone.utc)
                if exp_time < datetime.now(timezone.utc):
                    raise TokenError('Token expired')

                request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"

            except TokenError:
                new_access_token = self.refresh_access_token(refresh_token)
                if new_access_token:
                    request.META['HTTP_AUTHORIZATION'] = f"Bearer {new_access_token}"
                    request._new_access_token = new_access_token
                else:
                    request._clear_tokens = True
        else:
            pass

    def refresh_access_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            return str(refresh.access_token)
        except TokenError:
            return None

    def process_response(self, request, response):
        new_access_token = getattr(request, '_new_access_token', None)
        if new_access_token:
            access_expiry = AccessToken(new_access_token)['exp']
            response.set_cookie(
                key='access_token',
                value=new_access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=datetime.fromtimestamp(access_expiry, timezone.utc),
            )


        if getattr(request, '_clear_tokens', False):
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')

        return response
