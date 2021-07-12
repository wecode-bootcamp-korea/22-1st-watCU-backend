from django.urls import path, include

urlpatterns = [
    path('ratings', include('ratings.urls')),
    path('users', include('users.urls')),
    path('products', include('products.urls')),
    # path('comments', include('comments.urls')),
]
