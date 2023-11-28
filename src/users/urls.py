from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    SignupView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    # path("signup/<uidb64>/<token>/activate", ActivateView.as_view(), name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]