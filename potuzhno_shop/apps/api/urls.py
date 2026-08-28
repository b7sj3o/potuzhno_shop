from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "api"

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")
router.register("categories", views.CategoryViewSet, basename="category")
router.register("brands", views.BrandViewSet, basename="brand")
router.register("reviews", views.ReviewViewSet, basename="review")
router.register("sizes", views.SizeViewSet, basename="size")
urlpatterns = [
    path("", include(router.urls)),
    # path("token-auth/", obtain_auth_token),
    path('token/', views.ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.ThrottledTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('users/me/', views.MeView.as_view(), name='users_me'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]