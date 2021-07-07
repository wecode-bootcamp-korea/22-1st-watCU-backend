from operator import itemgetter

from django.http      import JsonResponse
from django.db.models import Avg
from django.views     import View

from django.db.models.aggregates import Avg

from products.models import Category, Product, Image
from ratings.models  import Rating

class MainView(View):
    def get(self, request):
        try:
            category = request.GET.get('category')
            results  = []

            if category == '전체':
                products = Product.objects.all()
            else:
                products = Product.objects.filter(category__name=category)
        
            for product in products:
                image_url = product.image_set.first().image_url
                
                if Rating.objects.filter(product=product).exists():        
                     average = Rating.objects.filter(product=product).aggregate(average=Avg('rating'))
                     average_rating = round(average['average'], 1)
                else:
                    average_rating = 0.0

                results.append(
                    {
                        'category_name'  : product.category.name,
                        'korean_name'    : product.korean_name,
                        'english_name'   : product.english_name,
                        'price'          : product.price,
                        'image_url'      : image_url,
                        'average_rating' : average_rating,
                        'description'    : product.description,
                    }
                )

            
            results = sorted(results, key=itemgetter('average_rating'), reverse=True)
            
            return JsonResponse({'results': results}, status=200)
        
        except Exception as error:
            return JsonResponse({'message': error}, status=400)

class DetailView(View):
    def get(self, request, product_id):
        try:
            page = request.GET.get('page')

            if page == 'detail':
                product  = Product.objects.get(id=product_id)
                category = product.category

                image_url = [image.image_url for image in product.image_set.all()]
           
                if Rating.objects.filter(product=product).exists():        
                        average = Rating.objects.filter(product=product).aggregate(average=Avg('rating'))
                        average_rating = round(average['average'], 1)
                else:
                    average_rating = 0.0

                result = {
                    'category_name'      : category.name,
                    'category_image_url' : category.image_url,
                    'korean_name'        : product.korean_name,
                    'english_name'       : product.english_name,
                    'price'              : product.price,
                    'description'        : product.description,
                    'main_image_url'     : image_url[0],
                    'sub_image_url'      : image_url[1:],
                    'average_rating'     : average_rating,
                    'description'        : product.description,
                }
        
                return JsonResponse({'result': result}, status=200)
            
            if page == 'related':
                results = []

                category  = Product.objects.get(id=product_id).category
                products  = Product.objects.filter(category=category).exclude(id=product_id)

                for product in products:
                    image_url = product.image_set.first().image_url

                    results.append(
                        {
                            'korean_name' : product.korean_name,
                            'english_name': product.english_name,
                            'price'       : product.price,
                            'image_url'   : image_url,
                        }
                    )
                
                return JsonResponse({'results': results}, status=200)
            
            return JsonResponse({'message': 'INVALID_REQUEST'}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXISTS'}, status=400)       
        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXISTS'}, status=400)       
        except Exception as error:
            return JsonResponse({'message': error}, status=400)