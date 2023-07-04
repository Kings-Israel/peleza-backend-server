from rest_framework import authentication
from rest_framework import exceptions, request as drf_request
from .models import PelClient


class ClientAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: drf_request.Request):
        BEARER_TOKEN: str = request.headers.get(
            "Authorization", request.GET.get("auth", "")
        )
        try:
            token = BEARER_TOKEN.replace("Bearer ", "").strip() if BEARER_TOKEN else ""

        except:
            token = None

        not_authenticated = exceptions.NotAuthenticated(
            detail={
                "status": {
                    "code": exceptions.NotAuthenticated().status_code,
                    "detail": exceptions.NotAuthenticated().default_detail,
                }
            }
        )
        authentication_failed = exceptions.AuthenticationFailed(
            detail={
                "status": {
                    "code": exceptions.AuthenticationFailed.status_code,
                    "detail": exceptions.AuthenticationFailed.default_detail,
                }
            }
        )

        #
        if BEARER_TOKEN == "" or BEARER_TOKEN == None or not BEARER_TOKEN:
            raise not_authenticated

        else:
            try:
                user = PelClient.objects.get(client_pin=token)
                if user:
                    data = (user, token)
                    return data
                raise authentication_failed

            except PelClient.DoesNotExist:
                raise authentication_failed

        raise not_authenticated
