from django.urls import path

from .views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    toggle_favourite,
    FavouriteListView,
)


app_name = "shop"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("favourite/toggle/<slug:slug>", toggle_favourite, name="toggle_favourite"),
    path("favourites/", FavouriteListView.as_view(), name="favourite_list"),
]
