from django.db.models.aggregates import Avg
from products.models import Category, Product

from django.http      import JsonResponse
from django.db.models import Avg
from django.views     import View

from products.models import Category, Product, Image
from ratings.models  import Rating

class MainView(View):
    def get(self, request):
        try:
            results = []

            for product in Product.objects.all():
                image_url = product.image_set.first().image_url
                
                if Rating.objects.filter(product=product).exists():        
                     average = Rating.objects.filter(product=product).aggregate(average=Avg('rating'))
                     average_rating = round(average['average'], 1)
                else:
                    average_rating = "0.0"

                results.append(
                    {
                        'category_name'  : product.category.name,
                        'korean_name'    : product.korean_name,
                        'english_name'   : product.english_name,
                        'price'          : product.price,
                        'image_url'      : image_url,
                        'average_rating' : average_rating,
                    }
                )
            
            return JsonResponse({'results': results}, status=200)
        
        except Exception as error:
            return JsonResponse({'message': error}, status=400)

class DetailView(View):
    def get(self, request, product_id):
        try:
            product   = Product.objects.get(id=product_id)
            image_url = product.image_set.first().image_url
                
            if Rating.objects.filter(product=product).exists():        
                     average = Rating.objects.filter(product=product).aggregate(average=Avg('rating'))
                     average_rating = round(average['average'], 1)
            else:
                average_rating = "0.0"

            result = {
                'category_name'  : product.category.name,
                'korean_name'    : product.korean_name,
                'english_name'   : product.english_name,
                'price'          : product.price,
                'description'    : product.description,
                'image_url'      : image_url,
                'average_rating' : average_rating,
            }
        
            return JsonResponse({'result': result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)       
        except Exception as error:
            return JsonResponse({'message': error}, status=400)