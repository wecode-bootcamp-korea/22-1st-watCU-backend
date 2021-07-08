from django.urls import path,include

urlpatterns = [
    path('ratings', include('ratings.urls')),
]
