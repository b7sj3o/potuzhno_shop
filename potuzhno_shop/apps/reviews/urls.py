from django.urls import path

from .views import (
    ReviewsHomeView
)

urlpatterns = [
    path("", ReviewsHomeView.as_view(), name="home"),
]
