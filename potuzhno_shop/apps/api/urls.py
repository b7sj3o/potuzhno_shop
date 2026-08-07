from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = "api"

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")
router.register("categories", views.CategoryViewSet, basename="category")
router.register("brands", views.BrandViewSet, basename="brand")
router.register("reviews", views.ReviewViewSet, basename="review")
urlpatterns = [
    path("", include(router.urls))
    # path("products/", views.ProductViewSet.as_view({'get': 'list', "post": "create"}), name="product-list"),
    # path("products/<int:pk>", views.ProductViewSet.as_view({'get': 'retrieve', "put": "update"}), name="product-detail")
]