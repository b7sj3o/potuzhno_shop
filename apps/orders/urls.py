from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.orders.views import OrderViewSet
from . import views  # додав імпорт views для усунення NameError

app_name = 'orders'

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # додав шлях до сторінки оформлення
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('', include(router.urls)),
]
