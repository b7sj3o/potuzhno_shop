import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from apps.shop.models import Category, Brand, Size, Product, Review
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem


# --- TYPES ---

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "created_at", "products")


class BrandType(DjangoObjectType):
    class Meta:
        model = Brand
        fields = ("id", "name", "slug", "products")


class SizeType(DjangoObjectType):
    class Meta:
        model = Size
        fields = ("id", "name")


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = ("id", "user", "product", "rating", "text", "created_at")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = (
            "id", "category", "brand", "name", "slug",
            "description", "price", "is_active", "is_featured",
            "sku", "audience", "stock", "sizes", "created_at",
            "updated_at", "reviews"
        )


class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ("id", "cart", "product", "quantity")


class CartType(DjangoObjectType):
    total_price = graphene.Float()

    class Meta:
        model = Cart
        fields = ("id", "user", "items")

    def resolve_total_price(self, info):
        return sum(item.product.price * item.quantity for item in self.items.all())


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = ("id", "order", "product", "quantity", "price")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = (
            "id", "user", "created_at", "status", "city",
            "post_office", "total_price", "phone",
            "customer_name", "items"
        )


# --- MUTATIONS ---

class AddToCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        quantity = graphene.Int(default_value=1)
        username = graphene.String(default_value="demo1")

    cart_item = graphene.Field(CartItemType)
    success = graphene.Boolean()

    def mutate(root, info, product_id, quantity, username):
        try:
            user = User.objects.get(username=username)
            cart, _ = Cart.objects.get_or_create(user=user)
            product = Product.objects.get(id=product_id, is_active=True)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product,
                defaults={"quantity": quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return AddToCart(cart_item=cart_item, success=True)
        except (User.DoesNotExist, Product.DoesNotExist):
            return AddToCart(cart_item=None, success=False)


class RemoveFromCart(graphene.Mutation):
    class Arguments:
        cart_item_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(root, info, cart_item_id):
        try:
            item = CartItem.objects.get(id=cart_item_id)
            item.delete()
            return RemoveFromCart(success=True)
        except CartItem.DoesNotExist:
            return RemoveFromCart(success=False)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_name = graphene.String(required=True)
        phone = graphene.String(required=True)
        city = graphene.String(required=True)
        post_office = graphene.String(required=True)
        username = graphene.String(default_value="demo1")

    order = graphene.Field(OrderType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(root, info, customer_name, phone, city, post_office, username):
        try:
            user = User.objects.get(username=username)
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.all()

            if not cart_items.exists():
                return CreateOrder(order=None, success=False, message="Кошик порожній!")

            total = sum(item.product.price * item.quantity for item in cart_items)

            order = Order.objects.create(
                user=user,
                customer_name=customer_name,
                phone=phone,
                city=city,
                post_office=post_office,
                total_price=total,
                status="new"
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Очищаємо кошик після успішного оформлення
            cart_items.delete()

            return CreateOrder(order=order, success=True, message="Замовлення успішно створено!")
        except (User.DoesNotExist, Cart.DoesNotExist) as e:
            return CreateOrder(order=None, success=False, message=str(e))


class Mutation(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
    remove_from_cart = RemoveFromCart.Field()
    create_order = CreateOrder.Field()


# --- QUERIES ---

class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    all_brands = graphene.List(BrandType)
    all_sizes = graphene.List(SizeType)
    all_products = graphene.List(ProductType, is_featured=graphene.Boolean(), audience=graphene.String())
    product_by_slug = graphene.Field(ProductType, slug=graphene.String(required=True))
    my_cart = graphene.Field(CartType, username=graphene.String(default_value="demo1"))
    my_orders = graphene.List(OrderType, username=graphene.String(default_value="demo1"))

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_all_brands(root, info):
        return Brand.objects.all()

    def resolve_all_sizes(root, info):
        return Size.objects.all()

    def resolve_all_products(root, info, is_featured=None, audience=None):
        qs = Product.objects.filter(is_active=True)
        if is_featured is not None:
            qs = qs.filter(is_featured=is_featured)
        if audience is not None:
            qs = qs.filter(audience=audience)
        return qs

    def resolve_product_by_slug(root, info, slug):
        try:
            return Product.objects.get(slug=slug, is_active=True)
        except Product.DoesNotExist:
            return None

    def resolve_my_cart(root, info, username):
        try:
            user = User.objects.get(username=username)
            cart, _ = Cart.objects.get_or_create(user=user)
            return cart
        except User.DoesNotExist:
            return None

    def resolve_my_orders(root, info, username):
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user)
        except User.DoesNotExist:
            return []


schema = graphene.Schema(query=Query, mutation=Mutation)
