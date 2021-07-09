from django.urls import path

from likes.views import StatusView

urlpatterns = [
    path('/<int:product_id>/status', StatusView.as_view()),
]
