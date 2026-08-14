from django_filters import rest_framework as filters

from apps.shop.models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    # /products?min_price=1000 -> price__gte = 1000
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = filters.CharFilter(field_name="category__name", lookup_expr="iexact")
    brand = filters.CharFilter(field_name="brand__name", lookup_expr="iexact")
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    in_stock = filters.BooleanFilter(method="filter_in_stock", label="Чи є в наявності")


    class Meta:
        model = Product
        fields = ["audience", "is_active", "is_featured"]


    def filter_in_stock(self, queryset, name, value):
        if value is True:
            return queryset.filter(stock__gt=0)
        if value is False:
            return queryset.filter(stock=0)
        return queryset
