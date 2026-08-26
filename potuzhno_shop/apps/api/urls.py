from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = "api"

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")
router.register("categories", views.CategoryViewSet, basename="category")
router.register("brands", views.BrandViewSet, basename="brand")
router.register("reviews", views.ReviewViewSet, basename="review")
urlpatterns = [
    path("", include(router.urls)),
    # path("token-auth/", obtain_auth_token),
    path('token/', views.ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.ThrottledTokenRefreshView.as_view(), name='token_refresh'),
]