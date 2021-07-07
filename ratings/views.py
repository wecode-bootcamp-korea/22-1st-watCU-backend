import json
from json.decoder import JSONDecodeError

from django.http      import JsonResponse
from django.views     import View

from users.models    import User
from products.models import Product
from ratings.models  import Rating

class RatingView(View):
    def post(self, request, product_id):
        try:
            data    = json.loads(request.body)
            user_id = data['user_id']

            user    = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            rating  = data['rating']

            if Rating.objects.filter(user=user, product=product).exists():
                Rating.objects.filter(user=user, product=product).update(
                    rating = rating
                )

                return JsonResponse({'message': 'RATING_MODIFIED_SUCCESS'}, status=201)
            
            Rating.objects.create(
                user    = user,
                product = product,
                rating  = rating,
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

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

    def delete(self, request, product_id):
        try:
            data    = json.loads(request.body)
            user_id = data['user_id']

            user    = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)

            if Rating.objects.filter(user=user, product=product).exists():
                Rating.objects.filter(user=user, product=product).delete()

            return JsonResponse({'message': 'SUCCESS'}, 201)

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
