from rest_framework import serializers

from apps.shop.models import Product, Category, Brand, Review, Size
from apps.shop.forms import unique_slug

# class ProductSerialzer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=200)
#     price = serializers.DecimalField(max_digits=10, decimal_places=2)
#     stock = serializers.IntegerField(min_value=0, required=False, default=0)
#     audience = serializers.ChoiceField(choices=Product.AUDIENCE_CHOICES)
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
#
#     def validate_price(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Ціна має бути більшою за 0.")
#         return value
#
#     def create(self, validated_data):
#         validated_data["slug"] = unique_slug(validated_data["name"])
#         return Product.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "created_at")
        read_only_fields = ("created_at",)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "slug")


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    sizes = serializers.SlugRelatedField( # [1, 3, 6] -> ["S", "XL", "L"]
        many=True, slug_field="name", queryset=Size.objects.all(), required=False,
    )
    avg_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price",
            "category", "category_name", "brand", "brand_name",
            "audience", "sizes", "stock", "sku",
            "is_active", "is_featured",
            "avg_rating", "reviews_count",
            "created_at", "updated_at",
        )
        read_only_fields = ("slug", "created_at", "updated_at")

    def get_avg_rating(self, obj):
        return getattr(obj, "avg_rating", None)

    def get_reviews_count(self, obj):
        return getattr(obj, "reviews_count", None)

    def create(self, validated_data):
        validated_data["slug"] = unique_slug(validated_data["name"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "name" in validated_data:
            validated_data["slug"] = unique_slug(validated_data["name"], instance=instance)
        return super().update(instance, validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "user", "username", "product", "rating", "text", "created_at")
        read_only_fields = ("created_at",)