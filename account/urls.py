from django.urls import path

from .views import RegisterView, LoginView, LogoutView, ActivationView

urlpatterns = [
    path('signup/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]