from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from apps.shop.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Product
        fields = '__all__'
        swagger_schema_fields = {
            "example": {
                "id": 1,
                "name": "Потужна футболка",
                "description": "Це дуже крута футболка",
                "price": 500.0,
                "category": {"id": 1, "name": "Одяг", "slug": "clothing"},
                "variants": [{"id": 1, "size": "M", "stock": 10}]
            }
        }