from django.urls import path

from products.views import MainView, DetailView

urlpatterns = [
    path('', MainView.as_view()),
    path('/<int:product_id>', DetailView.as_view()),
]
