from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


from apps.shop.models import Product, Category, Brand, Review

from .serializers import (
    ProductReadSerializer,
    ProductWriteSerializer,
    CategorySerializer,
    BrandSerializer,
    ReviewReadSerializer,
    ReviewWriteSerializer
)
from .permissions import IsOwnerOrStaffOrReadOnly, IsStaffOrReadOnly
from .pagination import StandardPagination
from .filters import ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReadSerializer
    permission_classes = (IsStaffOrReadOnly,)
    queryset = (
        Product.objects.with_rating()
        .select_related("category") # уникаємо N+1
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
    ordering_fields = ["created_at", "price", "name", "is_active"]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ProductReadSerializer
        return ProductWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.save()
        response = ProductReadSerializer(product, context=self.get_serializer_context())
        return Response(response.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def featured(self, request):
        products = self.filter_queryset(self.get_queryset()).filter(is_featured=True)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # products/<id>/reviews
    @action(detail=True, methods=["get"])
    def reviews(self, request, pk=None):
        # reviews = Review.objects.filter(product_id=pk)
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
    def favourite(self, request, pk=None):
        product = self.get_object()

        if request.user.profile.favourites.filter(id=pk).exists():
            return Response({"detail": "Product already added to your favourites"}, status=status.HTTP_200_OK)

        request.user.profile.favourites.add(product)
        return Response({"detail": "Product was added to your favourites"}, status=status.HTTP_201_CREATED)

    @favourite.mapping.delete
    def remove_favourite(self, request, pk=None):
        product = self.get_object()
        request.user.profile.favourites.remove(product)

        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)
    queryset = Category.objects.all()

class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = (IsStaffOrReadOnly,)
    queryset = Brand.objects.all()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "product")
    permission_classes = (IsOwnerOrStaffOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReviewReadSerializer
        return ReviewWriteSerializer


    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]\
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


