from django.urls import path

from ratings.views import RatingView

urlpatterns =[
    path('/products/<int:product_id>', RatingView.as_view()),
]
