from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product-api')

app_name = 'shop'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug:slug>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
