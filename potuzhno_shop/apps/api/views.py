import logging

from django.db.models import Exists, OuterRef, Value
from django.db.models.deletion import ProtectedError

from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.accounts.models import Profile
from apps.shop.models import Product, Category, Brand, Review, Size
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    ProductReadSerializer,
    ProductWriteSerializer,
    CategorySerializer,
    BrandSerializer,
    ReviewReadSerializer,
    ReviewWriteSerializer,
    SizeSerializer,
    RegisterSerializer,
    UserSerializer,
    ContactSerializer,
)
from .permissions import IsReviewsModeratorOrReadOnly, IsCatalogManagerOrReadOnly
from .pagination import StandardPagination
from .filters import ProductFilter

contact_logger = logging.getLogger("contact")

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReadSerializer
    permission_classes = (IsCatalogManagerOrReadOnly,)
    # SEO-дружні URL, як у шаблонах: /api/v1/products/<slug>/ замість /products/<id>/
    lookup_field = "slug"
    queryset = (
        Product.objects.with_rating()
        .select_related("category", "brand") # уникаємо N+1
        .prefetch_related("sizes")
    )
    pagination_class = StandardPagination
    filterset_class = ProductFilter
    # filterset_fields = ["is_active", "is_featured", "category__name"]
    # filterset_fields = {
    #     'name': ['icontains'],
    #     'price': ['gte', 'lte'],
    # }
    search_fields = [
        "name", # icontains
        "description",
        "=category__name", # iexact
        "^brand__name" # Adidas -> Adi
    ]
    ordering = ["-created_at", "-price"]
    ordering_fields = ["created_at", "price", "name", "is_active", "avg_rating"]


    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_authenticated:
            return qs.annotate(is_favourite=Exists(
                Profile.favourites.through.objects.filter(
                    product_id=OuterRef("pk"), profile__user=user
                )
            ))

        return qs.annotate(is_favourite=Value(False))

    def get_serializer_class(self):
        # Write-серіалізатор ТІЛЬКИ для мутацій. Стара умова
        # `if self.action in ("list", "retrieve")` віддавала read-серіалізатор
        # лише цим двом діям, тож кастомні @action (featured, favourites)
        # діставали ProductWriteSerializer — без slug/avg_rating і зі
        # stock/sku, які від не-staff мали бути приховані.
        if self.action in ("create", "update", "partial_update"):
            return ProductWriteSerializer
        return ProductReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.save()
        response = ProductReadSerializer(product, context=self.get_serializer_context())
        return Response(response.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # Як і в create: приймаємо write-серіалізатором, відповідаємо read-серіалізатором.
        # Інакше PATCH повертав би поля ProductWriteSerializer — без slug,
        # а фронтенду slug потрібен для редіректу (перейменування змінює slug).
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        product = serializer.save()
        response = ProductReadSerializer(product, context=self.get_serializer_context())
        return Response(response.data)

    @action(detail=False, methods=["get"])
    def featured(self, request):
        products = self.filter_queryset(self.get_queryset()).filter(is_featured=True)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # products/<slug>/reviews
    @action(detail=True, methods=["get"])
    def reviews(self, request, slug=None):
        product = self.get_object()
        reviews = (
            product.reviews
            .select_related("user")
            .order_by("-created_at")
        )

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewReadSerializer(page, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(serializer.data)

        serializer = ReviewReadSerializer(reviews, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated]
    )
    def favourite(self, request, slug=None):
        product = self.get_object()

        if request.user.profile.favourites.filter(pk=product.pk).exists():
            return Response({"detail": "Product already added to your favourites"}, status=status.HTTP_200_OK)

        request.user.profile.favourites.add(product)
        return Response({"detail": "Product was added to your favourites"}, status=status.HTTP_201_CREATED)

    @favourite.mapping.delete
    def remove_favourite(self, request, slug=None):
        product = self.get_object()
        request.user.profile.favourites.remove(product)

        return Response(status=status.HTTP_204_NO_CONTENT)

    # GET /products/favourites/ — обране поточного користувача (для сторінки профілю)
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def favourites(self, request):
        products = self.filter_queryset(self.get_queryset()).filter(
            favourited_by__user=request.user
        )

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class ProtectedDeleteMixin:
    """
    Category/Brand звʼязані з Product через on_delete=PROTECT: видалення запису,
    на який посилаються товари, кидає ProtectedError. Без цього міксина DRF
    відповів би 500 — перетворюємо на зрозумілий 409 Conflict.
    """

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "Неможливо видалити: на цей запис посилаються товари."},
                status=status.HTTP_409_CONFLICT,
            )

class CategoryViewSet(ProtectedDeleteMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    # Було IsAuthenticatedOrReadOnly: будь-який залогінений міг змінювати довідники
    permission_classes = (IsCatalogManagerOrReadOnly,)
    queryset = Category.objects.all()
    pagination_class = StandardPagination

class BrandViewSet(ProtectedDeleteMixin, viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = (IsCatalogManagerOrReadOnly,)
    queryset = Brand.objects.all()
    pagination_class = StandardPagination

class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    """Довідник розмірів — потрібен формі товару в React (чекбокси розмірів)."""
    serializer_class = SizeSerializer
    queryset = Size.objects.order_by("id")
    pagination_class = None  # розмірів мало — пагінація лише заважає

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "product")
    permission_classes = (IsReviewsModeratorOrReadOnly, )
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReviewReadSerializer
        return ReviewWriteSerializer


    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def mine(self, request):
        reviews = (
            self.get_queryset()
            .filter(user=request.user)
            .order_by("-created_at")
        )

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_scope = "login"


class ThrottledTokenRefreshView(TokenRefreshView):
    throttle_scope = "login"


class RegisterView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/ — аналог register() з apps.accounts.views.

    Шаблонна в'юшка після створення користувача одразу логінила його
    (login(request, user)). Для API "залогінити" = видати пару JWT-токенів,
    тому повертаємо їх разом із даними користувача.
    """

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "register"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": {"id": user.id, "username": user.username},
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET /api/v1/users/me/ — дані поточного користувача (аналог profile view).
    PATCH — оновлення email та phone/address з Profile.
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch", "head", "options"]

    def get_object(self):
        return self.request.user


class ContactView(APIView):
    """
    POST /api/v1/contact/ — аналог contact() з apps.shop.views.

    Як і шаблонна версія, нікуди не зберігає звернення — тільки пише в консоль
    (у шаблонах був print, тут — логер, як у сигналах accounts).
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        contact_logger.info(
            "CONTACT: name=%s email=%s subject=%s order=%s message=%s",
            data["name"], data["email"], data["subject"],
            data.get("order_number") or "-", data["message"],
        )

        return Response(
            {"detail": f"Дякуємо, {data['name']}! Ми відповімо на {data['email']}."},
            status=status.HTTP_200_OK,
        )