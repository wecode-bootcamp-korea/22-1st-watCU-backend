from django.urls import path

from ratings.views import RatingView, RatingGraphView, RatingCountView

urlpatterns =[
    path('', RatingCountView.as_view()),
    path('/products/<int:product_id>', RatingView.as_view()),
    path('/products/<int:product_id>/graph', RatingGraphView.as_view()),
]
