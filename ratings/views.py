import json, jwt

from json.decoder import JSONDecodeError

from django.http  import JsonResponse
from django.views import View

from my_settings import SECRET_KEY

from users.models    import User
from products.models import Product
from ratings.models  import Rating

from users.utils import ConfirmUser

class RatingView(View):
    @ConfirmUser
    def get(self, request, product_id):
        try:
            user    = request.user
            product = Product.objects.get(id=product_id)
            rating  = Rating.objects.get(user=user, product=product).rating
            
            result = {'rating': rating}        

            return JsonResponse({'result': result}, status=200)

        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)
        except jwt.DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXISTS'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)
        except Exception as error:
            return JsonResponse({'message': error}, status=400)

    @ConfirmUser
    def post(self, request, product_id):
        try:
            data    = json.loads(request.body)

            user    = request.user
            product = Product.objects.get(id=product_id)
            rating  = data['rating']
            
            object, is_created = Rating.objects.get_or_create(user=user, product=product, defaults={'rating': 0.0})
            object.rating = rating
            object.save()

            if is_created: 
                return JsonResponse({'message': 'SUCCESS'}, status=201)

            return JsonResponse({'message': 'MODIFIED_SUCCESS'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXISTS'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Exception as error:
            return JsonResponse({'message': error})

    @ConfirmUser
    def delete(self, request, product_id):
        try:
            user    = request.user
            product = Product.objects.get(id=product_id)

            if not Rating.objects.filter(user=user, product=product).exists():
                return JsonResponse({'message': 'INVALID_REQUEST'}, status=400)
            
            Rating.objects.filter(user=user, product=product).delete()

            return JsonResponse({'message': 'SUCCESS'}, status=204)

        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXISTS'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Exception as error:
            return JsonResponse({'message': error})

class RatingGraphView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            results = [{'rating': row.rating} for row in Rating.objects.filter(product=product).all()]

            return JsonResponse({'results': results}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except Exception as error:
            return JsonResponse({'message': error})