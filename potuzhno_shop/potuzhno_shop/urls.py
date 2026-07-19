from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.shop.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("orders/", include("apps.orders.urls")),

]
