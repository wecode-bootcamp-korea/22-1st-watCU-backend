import json
import re
import bcrypt
import jwt

from django.db.models.fields.json import JSONExact
from django.http                  import JsonResponse, request
from django.views                 import View
from django.core.exceptions       import ObjectDoesNotExist

from users.models                 import User
from users.validation             import email_validation, password_validation
from my_settings                  import SECRET_KEY                 

class SignUpView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            email          = data['email']
            name           = data['name']
            password       = data['password']
            hashed_pw      = bcrypt.hashpw( password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            duplicate_user = User.objects.filter(email = email).exists()
            
            if duplicate_user:
                return JsonResponse({"message" : "EMAIL_ALREADY_EXISTS"}, status = 400)

            if not email_validation(email):
                raise ValueError

            if not password_validation(password):
                raise ValueError

            user = User.objects.create(
                email    = email,
                name     = name,
                password = hashed_pw,
            )

            access_token   = jwt.encode({'user' : user.id}, SECRET_KEY, algorithm = 'HS256' )

            return JsonResponse({"token" : access_token}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "Key Error"}, status = 400)

        except ValueError:
            return JsonResponse({"message" : "Value Error"}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            email         = data['email']
            password      = data['password'].encode('utf-8')
            user          = User.objects.get(email = email)
            user_password = user.password.encode('utf-8')
            user_exists   = User.objects.filter(email = email).exists()
            access_token  = jwt.encode( {'user' : user.id}, SECRET_KEY, algorithm = 'HS256' )

            if user_exists:
                if bcrypt.checkpw(password, user_password):
                    return JsonResponse({"token" : access_token}, status = 200)
                
                else:
                    raise ValueError
            
            else :
                raise ObjectDoesNotExist

        except KeyError:
            return JsonResponse({"message" : "Key Error"}, status = 400)

        except ValueError:
            return JsonResponse({"message" : "Value Error"}, status = 400)

        except ObjectDoesNotExist:
            return JsonResponse({"message" : "Does Not Exist"}, status = 404)