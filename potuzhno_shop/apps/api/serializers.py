from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

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
    # Анотація з ProductViewSet.get_queryset(); для об'єктів без анотації — False
    is_favourite = serializers.BooleanField(read_only=True, default=False)
    # Точний stock бачить лише staff (див. to_representation),
    # але «є/немає в наявності» показуємо всім — як робили шаблони
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price",
            "category", "brand", "audience", "sizes",
            "stock", "sku", "is_active", "is_featured",
            "avg_rating", "reviews_count", "is_favourite", "in_stock",
            "created_at", "updated_at",
        )

    def get_in_stock(self, obj):
        return obj.stock > 0


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
        sizes = validated_data.pop("sizes") if "sizes" in validated_data else None
        validated_data["slug"] = unique_slug(validated_data["name"])

        product = Product.objects.create(**validated_data)
        if sizes:
            product.sizes.set(sizes)  # Обов'язково при M2M

        return product


    def update(self, instance, validated_data):
        if "name" in validated_data and validated_data["name"] != instance.name:
            validated_data["slug"] = unique_slug(validated_data["name"], instance=instance)
        return super().update(instance, validated_data)


class ProductMiniSerializer(serializers.ModelSerializer):
    """Мінімум даних про товар усередині відгуку — щоб фронтенд міг дати посилання."""

    class Meta:
        model = Product
        fields = ("id", "name", "slug")


class ReviewReadSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.StringRelatedField()
    # Було StringRelatedField (лише назва) — React-профілю потрібен slug для лінка
    product = ProductMiniSerializer(read_only=True)


    class Meta:
        model = Review
        fields = ("id", "user", "product", "rating", "text", "created_at")


class ReviewWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

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


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ("id", "name")


class RegisterSerializer(serializers.ModelSerializer):
    """Аналог RegisterForm(UserCreationForm) з apps.accounts.forms, але для API."""

    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("id", "username", "password", "password2")

    def validate_password(self, value):
        # Проганяє AUTH_PASSWORD_VALIDATORS — так само, як UserCreationForm
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Паролі не збігаються."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        # create_user хешує пароль; звичайний create зберіг би його відкритим текстом
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """GET/PATCH /users/me/ — дані User + поля Profile (phone, address)."""

    phone = serializers.CharField(
        source="profile.phone", max_length=20, allow_blank=True, required=False
    )
    address = serializers.CharField(
        source="profile.address", max_length=255, allow_blank=True, required=False
    )
    groups = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id", "username", "email", "phone", "address",
            "date_joined", "is_staff", "is_superuser", "groups",
        )
        read_only_fields = ("id", "username", "date_joined", "is_staff", "is_superuser")

    def update(self, instance, validated_data):
        # source="profile.*" складає вкладені поля у validated_data["profile"]
        profile_data = validated_data.pop("profile", {})
        instance = super().update(instance, validated_data)

        if profile_data:
            for field, value in profile_data.items():
                setattr(instance.profile, field, value)
            instance.profile.save()

        return instance


class ContactSerializer(serializers.Serializer):
    """Аналог ContactForm з apps.shop.forms: та сама валідація, ті самі теми."""

    SUBJECT_CHOICES = [
        ("product", "Питання про товар"),
        ("order", "Питання про замовлення"),
        ("delivery", "Доставка й оплата"),
        ("return", "Повернення / обмін"),
        ("other", "Інше"),
    ]

    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.ChoiceField(choices=SUBJECT_CHOICES)
    order_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    message = serializers.CharField()
    consent = serializers.BooleanField()

    def validate_message(self, value):
        message = value.strip()
        if len(message) < 10:
            raise serializers.ValidationError(
                "Повідомлення надто коротке — опишіть детальніше (мін. 10 символів)."
            )
        return message

    def validate_consent(self, value):
        if not value:
            raise serializers.ValidationError("Потрібна згода на обробку персональних даних.")
        return value

    def validate(self, attrs):
        if attrs["subject"] in ("order", "return") and not attrs.get("order_number"):
            raise serializers.ValidationError(
                {"order_number": "Для цієї теми вкажіть номер замовлення."}
            )
        return attrs