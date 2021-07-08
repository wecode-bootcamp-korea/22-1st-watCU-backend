import json

from django.db.models.expressions import Exists
from products.models import Category, Product

from django.http     import JsonResponse
from django.views    import View
from django.db       import DataError

from products.models import Category, Product
from users.models    import User
from likes.models    import Done, Wish, Like
from users.utils     import ConfirmUser

class WishView(View):
    # 먹고싶어요
    @ConfirmUser
    def get(self, request, product_id):
        try:
            user = request.user
            filter_like = Wish.objects.filter(product_id=product_id).filter(user_id=user.id).exists()
            if not filter_like:
                Wish.objects.create(
                    user_id     = user.id,
                    product_id  = product_id
                    )
                
                return JsonResponse({'results': 'Success'}, status=201)
            
            else:
                raise ValueError
    
        except Exception as error:
            return JsonResponse({'message': error}, status=400)

    # 먹고싶어요 삭제
    @ConfirmUser
    def delete(self, request, product_id):
        try:
            user = request.user
            filter_like = Wish.objects.filter(product_id=product_id).filter(user_id=user.id)

            if filter_like.exists:
                filter_like.delete()
                return JsonResponse({'results': 'Success'}, status=201)
            
            else:
                raise ValueError
    
        except Exception as error:
            return JsonResponse({'message': error}, status=400)
            
class DoneView(View):
    # 먹어봤어요
    @ConfirmUser
    def get(self, request, product_id):
        try:
            user = request.user
            filter_like = Done.objects.filter(product_id=product_id).filter(user_id=user.id).exists()

            if not filter_like:
                Done.objects.create(
                    user_id     = user.id,
                    product_id  = product_id,
                    )
                
                return JsonResponse({'results': 'Success'}, status=201)
            
            else:
                raise ValueError
    
        except Exception as error:
            return JsonResponse({'message': error}, status=400)

    # 먹어봤어요 삭제
    @ConfirmUser
    def delete(self, request, product_id):
        try:
            user = request.user
            filter_like = Done.objects.filter(product_id=product_id).filter(user_id=user.id)

            if filter_like.exists:
                filter_like.delete()
                return JsonResponse({'results': 'Success'}, status=201)
            
            else:
                raise ValueError
    
        except Exception as error:
            return JsonResponse({'message': error}, status=400)

class LikeView(View):
    #댓글 좋아요
    @ConfirmUser
    def get(self, request, comment_id):
        try:
            user = request.user
            filter_like = Done.objects.filter(comment_id=comment_id).filter(user_id=user.id).exists()

            if not filter_like:
                Done.objects.create(
                    user_id     = user.id,
                    comment_id  = comment_id,
                    )
                
                return JsonResponse({'results': 'Success'}, status=201)
            
            else:
                raise ValueError
    
        except Exception as error:
            return JsonResponse({'message': error}, status=400)

    # 댓글 좋아요 삭제
    @ConfirmUser
    def delete(self, request, comment_id):
        try:
            user = request.user
            filter_like = Done.objects.filter(comment_id=comment_id).filter(user_id=user.id)

            if filter_like.exists:
                filter_like.delete()
                return JsonResponse({'results': 'Success'}, status=201)
            
            else:
                raise ValueError
    
        except Exception as error:
            return JsonResponse({'message': error}, status=400)