import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType

from apps.shop.models import Product, Brand, Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class BrandType(DjangoObjectType):
    class Meta:
        model = Brand
        fields = ("id", "name", "slug")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price", "category", "brand",
            "audience", "is_featured", "created_at"
        )

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product = graphene.Field(ProductType, slug=graphene.String(required=True) )
    all_categories = graphene.List(CategoryType)

    def resolve_all_products(self, info):
        return Product.objects.filter(is_active=True).select_related("category", "brand")

    def resolve_product(self, info, slug):
        return Product.objects.get(slug=slug)

    def resolve_all_categories(self, info):
        return Category.objects.all()


class AddToFavourite(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)

    ok = graphene.Boolean()
    product = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, slug):
        user = info.context.user

        if not user.is_authenticated:
            raise GraphQLError("Потрібно увійти в акаунт, щоб керувати улюбленими товарами")

        product = Product.objects.filter(slug=slug).first()
        if product is None:
            raise GraphQLError("Товар не знайдено")

        user.profile.favourites.add(product)

        return AddToFavourite(
            ok=True,
            product=product
        )


class RemoveFromFavourite(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)

    ok = graphene.Boolean()
    product = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, slug):
        user = info.context.user

        if not user.is_authenticated:
            raise GraphQLError("Потрібно увійти в акаунт, щоб керувати улюбленими товарами")

        product = Product.objects.filter(slug=slug).first()
        if product is None:
            raise GraphQLError("Товар не знайдено")

        user.profile.favourites.remove(product)

        return AddToFavourite(
            ok=True,
            product=product
        )


class Mutation(graphene.ObjectType):
    add_to_favourite = AddToFavourite.Field()
    remove_from_favourite = RemoveFromFavourite.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)