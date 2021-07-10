from django.urls import path
from users.views import LoginView, SignUpView, SearchView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/search', SearchView.as_view()),
]
