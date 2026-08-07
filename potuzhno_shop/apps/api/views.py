from rest_framework import status, viewsets, permissions, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.shop.models import Product, Category, Brand, Review

from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, ReviewSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = (
        Product.objects.with_rating()
        .select_related("category")
        .prefetch_related("sizes")
    )


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class ReviewViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related("user", "product")


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
