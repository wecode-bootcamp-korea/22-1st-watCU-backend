from django.urls import path

from likes.views import WishView, DoneView, LikeView

urlpatterns = [
    path('/wish/<int:product_id>', WishView.as_view()),
    path('/done/<int:product_id>', DoneView.as_view()),
    path('/<int:product_id>', LikeView.as_view()),
]
