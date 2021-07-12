from django.urls import path

from products.views import ProductView, PrivateProductView, ProductDetailView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/private', PrivateProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]