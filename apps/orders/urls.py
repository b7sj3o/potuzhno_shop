from django.urls import path
from .views import OrderStatisticsView

urlpatterns = [
    path('stats/', OrderStatisticsView.as_view(), name='order-stats'),
]
