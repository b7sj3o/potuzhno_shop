from rest_framework import serializers

from apps.shop.models import Product, Category, Brand, Review, Size
from apps.shop.forms import unique_slug


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "created_at")
        read_only_fields = ("created_at",)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "slug")


class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    sizes = serializers.SlugRelatedField( # [1, 3, 6] -> ["S", "XL", "L"]
        many=True, slug_field="name", read_only=True
    )
    avg_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price",
            "category", "brand", "audience", "sizes",
            "stock", "sku", "is_active", "is_featured",
            "avg_rating", "reviews_count", "created_at", "updated_at",
        )


    def get_avg_rating(self, obj):
        return getattr(obj, "avg_rating", 0)

    def get_reviews_count(self, obj):
        return getattr(obj, "reviews_count", 0)


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")

        if not (request and request.user.is_staff):
            representation.pop("sku", None)
            representation.pop("stock", None)

        return representation


class ProductWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "id", "name", "description", "price",
            "category", "brand", "audience", "sizes",
            "stock", "sku", "is_active", "is_featured",
            "created_at", "updated_at",
        )

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Ціна має бути більшою за 0.")
        return price


    def validate_stock(self, stock):
        if stock < 0:
            raise serializers.ValidationError("К-сть товару не може бути від'ємною.")
        return stock


    def validate(self, attrs):
        is_featured = attrs.get("is_featured", getattr(self.instance, "is_featured", False))
        stock = attrs.get("stock", getattr(self.instance, "stock", 0))

        if is_featured and stock == 0:
            raise serializers.ValidationError({
                "is_featured": "Не можна рекомендувати товар, якого немає в наявності.",
            })

        return attrs


    def create(self, validated_data):
        sizes = validated_data.pop("sizes")
        validated_data["slug"] = unique_slug(validated_data["name"])

        product = Product.objects.create(**validated_data)
        product.sizes.set(sizes)  # Обов'язково при M2M

        return product


    def update(self, instance, validated_data):
        if "name" in validated_data and validated_data["name"] != instance.name:
            validated_data["slug"] = unique_slug(validated_data["name"], instance=instance)
        return super().update(instance, validated_data)


class ReviewReadSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()


    class Meta:
        model = Review
        fields = ("id", "user", "product", "rating", "text", "created_at")


class ReviewWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.ChoiceField(choices=Product.objects.all())

    class Meta:
        model = Review
        fields = ("id", "user", "product", "rating", "text", "created_at")
        read_only_fields = ("created_at",)



    def validate(self, attrs):
        rating = attrs.get("rating", getattr(self.instance, "rating", 5))
        text = attrs.get("text", getattr(self.instance, "text", "")).strip()

        if rating <= 2 and len(text) < 5:
            raise serializers.ValidationError({
                "text": "Для оцінки 1–2 поясніть, що не сподобалось (мінімум 5 символів).",
            })

        return attrs




# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = ('id', 'username')
#
#
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('id', 'name')
#
#
# class PostSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer(read_only=True)
#     tags = TagSerializer(many=True, read_only=True)
#     # depth = 1
#
#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'author', 'tags')


# PostSerializer(Post.objects.all(), many=True).data
# → 23 запити до БД при 11 постах
#
# PostSerializer(
#     Post.objects.select_related('author').prefetch_related('tags'),
#     many=True
# ).data
# → 2 запити

# GET /post/1
# {
#   "id": 1,
#   "title": "Про Django",
#   "author": {"id": 5, "username": "alex"},
#   "tags": [{"id": 10, "name": "python"}, {"id": 12, "name": "django"}]
# }