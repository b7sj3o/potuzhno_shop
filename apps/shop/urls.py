from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, product_update, product_list, product_detail

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', product_list, name='product_list'),
    path('products/<slug:slug>/', product_detail, name='product_detail'),
    path('products/<slug:slug>/edit/', product_update, name='product_update'),
] + router.urls
