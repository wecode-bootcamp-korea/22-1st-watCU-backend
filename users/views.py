import json
import re
import bcrypt
import jwt

from django.db.models.fields.json import JSONExact
from django.http                  import JsonResponse, request
from django.views                 import View
from django.core.exceptions       import ObjectDoesNotExist

from products.models              import Product, Category
from users.models                 import User
from users.validation             import email_validation, password_validation
from my_settings                  import SECRET_KEY,ALGORITHM                

class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            email           = data['email']
            name            = data['name']
            password        = data['password']
            hashed_password = bcrypt.hashpw( password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            duplicate_user  = User.objects.filter(email = email).exists()
            
            if duplicate_user:
                return JsonResponse({"message" : "EMAIL_ALREADY_EXISTS"}, status = 400)

            if not email_validation(email):
                raise ValueError

            if not password_validation(password):
                raise ValueError

            user = User.objects.create(
                email    = email,
                name     = name,
                password = hashed_password,
            )

            access_token = jwt.encode({'user' : user.id}, SECRET_KEY, algorithm = ALGORITHM)

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
            access_token  = jwt.encode( {'user' : user.id}, SECRET_KEY, algorithm = ALGORITHM)

            if user:
                if bcrypt.checkpw(password, user_password):
                    return JsonResponse({"token" : access_token}, status = 201)
                
                raise ValueError

            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message" : "Key Error"}, status = 400)

        except ValueError:
            return JsonResponse({"message" : "Value Error"}, status = 400)

class SearchView(View):
    def get(self, request):
        try:
            word = request.GET.get('word', '')
            results=[]

            korean_name   = Product.objects.filter(korean_name__icontains = word).exists()
            english_name  = Product.objects.filter(english_name__icontains = word).exists()
            category_name = Category.objects.filter(name__icontains = word).exists()

            if korean_name:
                products  = Product.objects.filter(korean_name__icontains = word)
                for product in products:
                    results.append({
                        'word' : product.korean_name
                    })

            if english_name:
                products  = Product.objects.filter(english_name__icontains = word)
                for product in products:
                    results.append({
                        'word' : product.english_name
                    })

            if category_name:
                categories = Category.objects.filter(name__icontains = word)
                for category in categories:
                    results.append({
                        'word' : category.name
                    })
            
            return JsonResponse({'results': results}, status=200)
        
        except KeyError:
            return JsonResponse({"message" : "Key Error"}, status = 400)

        except ValueError:
            return JsonResponse({"message" : "Value Error"}, status = 400)