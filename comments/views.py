import json

from django.core      import exceptions
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from django.db.utils  import DataError

from comments.models  import Comment
from users.models     import User
from products.models  import Product
from users.utils      import ConfirmUser

class CommentView(View):
    @ConfirmUser
    def post(self, request):
        try:
            data    = json.loads(request.body)
            content = data['content']
            product = data['product_id']
            comment = request.GET.get('comment-id', '')
            user    = request.user

            if comment:
                if Comment.objects.get(id = comment).product_id != product:
                    raise DataError

            Comment.objects.create(
            content           = content,
            product_id        = product,
            user              = user,
            parent_comment_id = comment if comment else None,
            )

            return JsonResponse({'results': 'Success'}, status=201)

        except DataError:
            return JsonResponse({'message': 'DataError'}, status=400)      

        except ValueError:
            return JsonResponse({'message': 'ValueError'}, status=400)        
    
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
    
    def get(self, request, product_id):
        try:
            comments = Comment.objects.filter(product_id=product_id)

            results = [{
                "id"             : comment.id,
                "name"           : comment.user.name,
                "rating"         : (comment.user.rating_set.get(product_id=product_id).rating 
                                    if comment.user.rating_set.filter(product_id=product_id).exists()
                                    else 0) ,
                "content"        : comment.content,
                "like"           : comment.like_set.count(),
                "nested_comment" : comment.child_comment.count(),
            } for comment in comments]

            return JsonResponse({'results': results}, status=200)

        except ValueError:
            return JsonResponse({'message': 'ValueError'}, status=400)        
    
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'Invalid comment'}, status=404)

    @ConfirmUser
    def patch(self, request, comment_id):
        try:
            data    = json.loads(request.body)
            content = data['content']
            user    = request.user
            
            Comment.objects.filter(user=user).filter(id=comment_id).update(content = content)

            return JsonResponse({'results': 'Success'}, status=201)

        except Comment.DoesNotExist:
            return JsonResponse({'message': 'Invalid comment'}, status=404)
    
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)

    @ConfirmUser
    def delete(self, request, comment_id):
        try:
            Comment.objects.get(id=comment_id).delete()

            return JsonResponse({'results': 'Delete Success'}, status=204)
        
        except Comment.DoesNotExist:
            return JsonResponse({'message': 'Invalid comment'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)

class NestedCommentView(View):
    def get(self,request, comment_id):
        try:
            if Comment.objects.filter(Q(id = comment_id)&~Q(parent_comment_id=None)):
                raise DataError

            product_id = Comment.objects.get(id = comment_id).product.id
            comments   = Comment.objects.filter(parent_comment_id=comment_id)

            results = [{
                "id"             : comment.id,
                "name"           : comment.user.name,
                "rating"         : (comment.user.rating_set.get(product_id=product_id).rating 
                                    if comment.user.rating_set.filter(product_id=product_id).exists()
                                    else 0) ,
                "content"        : comment.content,
                "like"           : comment.like_set.count(),
            } for comment in comments]

            return JsonResponse({'results': results}, status=200)

        except DataError:
            return JsonResponse({'message': 'DataError'}, status=400)  

        except ValueError:
            return JsonResponse({'message': 'ValueError'}, status=400)        
    
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)

        except Comment.DoesNotExist:
            return JsonResponse({'message': 'Invalid comment'}, status=404)