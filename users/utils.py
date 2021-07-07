import jwt
import json

from django.http    import JsonResponse
from jwt.exceptions import DecodeError

from my_settings    import SECRET_KEY
from users.models   import User

class ConfirmUser:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *arg, **kargs):
        try:
            access_token     = request.headers.get('Athorization', None)

            if access_token:
                payload      = jwt.decode( access_token, SECRET_KEY, algorithms = 'HS256' )
                login_user   = User.objects.get(id = payload['user'])
                request.user = login_user
                return self.func(self, request, *arg, **kargs)
            
            else:
                return JsonResponse({"message" : "NEED LOGIN"}, status = 401)
                
        except DecodeError:
            return JsonResponse({"message" : "INVALLED TOKEN"}, status = 401)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALLED USER"}, status = 401)
