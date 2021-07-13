from django.urls import path

from ratings.views import RatingView, RatingGraphView

urlpatterns =[
    path('/products/<int:product_id>', RatingView.as_view()),
    path('/products/<int:product_id>/graph', RatingGraphView.as_view()),
]
