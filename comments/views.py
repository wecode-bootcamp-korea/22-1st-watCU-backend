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
            user    = request.user
            
            Comment.objects.create(
                content    = content,
                product_id = product,
                user       = user
            )

            return JsonResponse({'results': 'Success'}, status=201)
        
        except ValueError:
            return JsonResponse({'message': 'ValueError'}, status=400)        
    
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
    
    def get(self, request):
        try:
            product_id = request.GET.get('product_id', '')

            comments = Comment.objects.filter(product_id=product_id)
            results = []

            for comment in comments:
                if not comment.parent_comment:
                    if comment.user.rating_set.filter(product_id=product_id).exists():
                        results.append({
                            "id"             : comment.id,
                            "name"           : comment.user.name,
                            "rating"         : comment.user.rating_set.get(product_id=product_id).rating,
                            "content"        : comment.content,
                            "like"           : comment.like_set.count(),
                            "nested_comment" : comment.child_comment.count(),
                        })
                    
                    else:
                        results.append({
                            "id"             : comment.id,
                            "name"           : comment.user.name,
                            "rating"         : 0,
                            "content"        : comment.content,
                            "like"           : comment.like_set.count(),
                            "nested_comment" : comment.child_comment.count(),
                        })
            
            return JsonResponse({'results': 'Success'}, status=200)

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
    @ConfirmUser
    def post(self, request, comment_id):
        try:
            data           = json.loads(request.body)
            content        = data['content']
            user           = request.user
            parent_comment = Comment.objects.get(id=comment_id)

            Comment.objects.create(
                content        = content,
                parent_comment = parent_comment,
                product        = parent_comment.product,
                user           = user
            )

            return JsonResponse({'results': 'Success'}, status=201)
    
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'ValueError'}, status=400)

    def get(self, request, comment_id):
        try:
            parent_comment = Comment.objects.get(id=comment_id)
            comments       = Comment.objects.filter(parent_comment=parent_comment)
            product_id     = parent_comment.product.id
            results        = []

            for comment in comments:
                if not comment.parent_comment:
                    if comment.user.rating_set.filter(product_id=product_id).exists():
                        results.append({
                            "id"             : comment.id,
                            "name"           : comment.user.name,
                            "rating"         : comment.user.rating_set.get(product_id=product_id).rating,
                            "content"        : comment.content,
                            "like"           : comment.like_set.count(),
                        })
                    
                    else:
                        results.append({
                            "id"             : comment.id,
                            "name"           : comment.user.name,
                            "rating"         : 0,
                            "content"        : comment.content,
                            "like"           : comment.like_set.count(),
                        })

            return JsonResponse({'results': results}, status=200)

        except Comment.DoesNotExist:
            return JsonResponse({'message': 'Invalid comment'}, status=404)

        except KeyError:
            return JsonResponse({'message': "Key Error"}, status=400)