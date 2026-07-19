from django.urls import path

from .views import (
    OrdersHomeView
)

urlpatterns = [
    path("", OrdersHomeView.as_view(), name="home"),
]
