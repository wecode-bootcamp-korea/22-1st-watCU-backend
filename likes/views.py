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
            data    = json.loads(request.body)
            user    = request.user
            status  = data["status"]

            status_object , created = Status.objects.get_or_create(
                status              = status,
                user_id             = user.id,
                product_id          = product_id
            )

            if not created:
                status_object.delete()

                return JsonResponse({'results': f'Delete {status}'}, status=201)

            return JsonResponse({'results': f'Create {status}'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)

class LikeView(View):
    # 댓글 좋아요 생성
    @ConfirmUser
    def post(self, request, comment_id):
        try:
            user            = request.user

            like, create = Like.objects.get_or_create(
                user_id     = user.id,
                comment_id  = comment_id,
            )
            
            if not create:
                like.delete()
                
                return JsonResponse({'results': 'unlike'}, status=201)
            
            return JsonResponse({'results': 'like'}, status=201)
            
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)