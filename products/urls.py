from django.urls import path

from likes.views import WishView, DoneView

urlpatterns = [
    path('/<int:product_id>/wish', WishView.as_view()),
    path('/<int:product_id>/done', DoneView.as_view()),

]
