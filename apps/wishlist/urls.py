from django.urls import path
from .views import wishlist_detail, add_to_wishlist, remove_from_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_detail, name='wishlist_detail'),
    path('add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
