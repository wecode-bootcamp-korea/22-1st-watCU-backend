from operator import itemgetter

from django.http      import JsonResponse
from django.db.models import Avg
from django.views     import View

from django.db.models.aggregates import Avg

from products.models import Category, Product, Image
from ratings.models  import Rating

class ProductView(View):
    def get(self, request):
        try:
            category = request.GET.get('category', '')
            products = Product.objects.filter(category__name__startswith=category)

            results = [
                {
                    'category_name'  : product.category.name,
                    'korean_name'    : product.korean_name,
                    'english_name'   : product.english_name,
                    'price'          : product.price,
                    'image_url'      : product.image_set.first().image_url,
                    'product_id'     : product.id,
                    'average_rating' : ( round(Rating.objects.filter(product=product).aggregate(average=Avg('rating'))['average'], 1)
                                            if Rating.objects.filter(product=product).exists()
                                            else 0.0 )
                }

                for product in products
            ]
                
            results = sorted(results, key=itemgetter('average_rating'), reverse=True)
            
            return JsonResponse({'results': results}, status=200)
        
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
            category = product.category

            image_urls = [image.image_url for image in product.image_set.all()]
            average_rating = ( round(Rating.objects.filter(product=product).aggregate(average=Avg('rating'))['average'], 1)
                                if Rating.objects.filter(product=product).exists()
                                else 0.0 )

            result = {
                'category_name'      : category.name,
                'category_image_url' : category.image_url,
                'korean_name'        : product.korean_name,
                'english_name'       : product.english_name,
                'price'              : product.price,
                'description'        : product.description,
                'main_image_url'     : image_urls[0],
                'sub_image_url'      : image_urls[1:],
                'average_rating'     : average_rating,
                'description'        : product.description,
            }
    
            return JsonResponse({'result': result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)       
        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXISTS'}, status=400)       
        except Exception as error:
            return JsonResponse({'message': error}, status=400)