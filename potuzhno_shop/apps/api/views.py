from rest_framework import status, viewsets, permissions, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

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


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReadSerializer
    permission_classes = (IsStaffOrReadOnly,)
    queryset = (
        Product.objects.with_rating()
        .select_related("category") # уникаємо N+1
        .prefetch_related("sizes")
    )

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


# class ProductListCreateApiView(APIView):
#     def get(self, request):
#         products = Product.objects.active()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

