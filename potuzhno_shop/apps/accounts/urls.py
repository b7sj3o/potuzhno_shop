from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    AccountsHomeView,
    LoginView,
    register,
    profile,
)



app_name = "accounts"

urlpatterns = [
    path("", AccountsHomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", register, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
]
