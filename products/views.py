from operator import itemgetter

from django.http      import JsonResponse
from django.db.models import Avg
from django.views     import View

from django.db.models.aggregates import Avg

from products.models import Category, Product, Image
from ratings.models  import Rating

from users.utils import ConfirmUser

from users.models import User

class ProductView(View):
    def get(self, request):
        try:
            category_name = request.GET.get('category', '')
            product_id    = request.GET.get('product_id', None)

            products = Product.objects.filter(category__name__startswith=category_name).exclude(id=product_id)
            products = products.annotate(average_rating=Avg('rating__rating')).order_by('-average_rating')

            results = [
                {
                    'category_name'  : product.category.name,
                    'korean_name'    : product.korean_name,
                    'english_name'   : product.english_name,
                    'price'          : product.price,
                    'image_url'      : product.image_set.first().image_url if product.image_set.exists() else None,
                    'product_id'     : product.id,
                    'category_id'    : product.category.id,
                    'average_rating' : round(product.average_rating, 1) if product.average_rating else 0.0,
                    'badge'          : i + 1,
                }

                for i, product in enumerate(products)
            ]
                
            return JsonResponse({'results': results}, status=200)
        
        except Image.DoesNotExist:
            return JsonResponse({'message': 'IMAGE_DOES_NOT_EXISTS'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)
        except Exception as error:
            return JsonResponse({'message': error}, status=400)

class PrivateProductView(View):
    # @ConfirmUser
    def get(self, request):
        try:
            limit  = int(request.GET.get('limit', 100))
            offset = int(request.GET.get('offset', 0))
            
            # user = request.user
            user = User.objects.get(id=1)

            category_name = request.GET.get('category', '')
            products = Product.objects.filter(category__name__startswith=category_name)

            start_index = (limit*offset) % len(products)
            end_index   = len(products) if (limit*(offset+1)) % len(products) == 0 else (limit*(offset+1)) % len(products)

            products = products.annotate(average_rating=Avg('rating__rating')).order_by('-average_rating')[start_index:end_index]

            results = [
                {
                    'category_name'  : product.category.name,
                    'korean_name'    : product.korean_name,
                    'english_name'   : product.english_name,
                    'price'          : product.price,
                    'image_url'      : product.image_set.first().image_url if product.image_set.exists() else None,
                    'product_id'     : product.id,
                    'category_id'    : product.category.id,
                    'average_rating' : round(product.average_rating, 1) if product.average_rating else 0.0
                }

                for product in products
            ]

            rating_count = Rating.objects.filter(user=user, product__category__name__startswith=category_name).count()
            
            return JsonResponse({'results': results,
                                 'rating_count': rating_count
                                 }, status=200)
        
        except Image.DoesNotExist:
            return JsonResponse({'message': 'IMAGE_DOES_NOT_EXISTS'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)
        except Exception as error:
            return JsonResponse({'message': error}, status=400)
    


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product  = Product.objects.get(id=product_id)

            image_urls = [image.image_url for image in product.image_set.all()] if product.image_set else []
            average_rating = ( round(Rating.objects.filter(product=product).aggregate(average=Avg('rating'))['average'], 1)
                                if Rating.objects.filter(product=product).exists()
                                else 0.0 )

            result = {
                'category_name'      : product.category.name,
                'category_image_url' : product.category.image_url,
                'korean_name'        : product.korean_name,
                'english_name'       : product.english_name,
                'price'              : product.price,
                'description'        : product.description,
                'main_image_url'     : image_urls[0] if image_urls else [],
                'sub_image_url'      : image_urls[1:] if len(image_urls) > 1 else [],
                'average_rating'     : average_rating,
            }
    
            return JsonResponse({'result': result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)       
        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXISTS'}, status=400)       
        except Exception as error:
            return JsonResponse({'message': error}, status=400)