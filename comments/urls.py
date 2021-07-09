
from django.urls import path

from likes.views import LikeView

urlpatterns = [
    path('/<int:comment_id>/like', LikeView.as_view()),
]
