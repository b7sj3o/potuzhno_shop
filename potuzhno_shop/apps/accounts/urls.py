from django.urls import path

from .views import (
    AccountsHomeView,
    FavouriteToggleView,
    FavouritesView
)
app_name = "accounts"

urlpatterns = [
    path("", AccountsHomeView.as_view(), name="home"),
    path("favorites/toggle/<slug:slug>/", FavouriteToggleView.as_view(), name="favourite_toggle"),
    path("favorites/", FavouritesView.as_view(), name="favourites"),
]
