import json

from django.db.models.expressions import Exists
from django.db.models.fields      import CharField

from django.http                  import JsonResponse
from django.views                 import View
from django.db                    import DataError
from django.db.models             import Q

from products.models              import Category, Product
from users.models                 import User
from likes.models                 import Status, Like
from users.utils                  import ConfirmUser

class StatusView(View):
    # 먹고싶어요 먹어봤어요 상태 생성
    @ConfirmUser
    def post(self, request, product_id):
        try:
            data       = json.loads(request.body)
            user       = request.user
            status     = data['status']
            
            Status.objects.create(
                status     = status,
                user_id    = user.id,
                product_id = product_id
            )

            return JsonResponse({'results': 'Success'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
            
    # 먹고싶어요 먹어봤어요 상태 삭제
    @ConfirmUser
    def delete(self, request, product_id):
        try:
            status  = request.GET.get('status', '')
            user    = request.user

            Status.objects.filter(user_id=user.id).filter(product_id=product_id).get(status=status).delete()

            return JsonResponse({'results': 'Success'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
            
class LikeView(View):
    # 댓글 좋아요 생성
    @ConfirmUser
    def get(self, request):
        try:
            comment     = request.GET.get('comment', '')
            user        = request.user
            like_user   = Like.objects.filter(comment_id=comment).filter(user_id=user.id).exists()

            if not like_user:
                Like.objects.create(
                    user_id     = user.id,
                    comment_id  = comment,
                    )
                
                return JsonResponse({'results': 'Success'}, status=201)
            
            else:
                raise ValueError
    
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)

    # 댓글 좋아요 삭제
    @ConfirmUser
    def delete(self, request):
        try:
            comment = request.GET.get('comment','')
            user    = request.user
            like    = Like.objects.filter(comment_id=comment).get(user_id=user.id)

            like.delete()
            return JsonResponse({'results': 'Success'}, status=201)
    
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
