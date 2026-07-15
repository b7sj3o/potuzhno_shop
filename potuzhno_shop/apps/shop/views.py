from django.http import  Http404
from django.db.models import Q, F
from django.views.generic import TemplateView, ListView, DetailView


from .models import Product, Category


class HomeView(TemplateView):
    template_name = "shop/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured"] = Product.objects.filter(is_featured=True).with_rating()[:3]

        return context


class ProductListView(ListView):
    template_name = "shop/product_list.html"
    context_object_name = "products"
    model = Product
    paginate_by = 10

    SORT_MAP = {
        "price": F("price").asc(),
        "-price": F("price").desc(),
        "name": F("name").asc(),
        "-avg_rating": F("avg_rating").desc(nulls_last=True),
    }

    def get_queryset(self):
        qs = (
            Product.objects.active()
            .with_rating()
            .select_related("category")
            .prefetch_related("sizes")
        )
        params = self.request.GET

        q = params.get("q", "")
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(brand__name__icontains=q)
                | Q(category__name__icontains=q)
            )

        category = params.get("category", "")
        if category:
            qs = qs.filter(category__slug=category)

        audience = params.get("audience", "")
        if audience:
            qs = qs.filter(audience=audience)

        min_price = params.get("min_price", "")
        if min_price:
            qs = qs.filter(price__gte=min_price)

        max_price = params.get("max_price", "")
        if max_price:
            qs = qs.filter(price__lte=max_price)

        min_rating = params.get("min_rating", "")
        if min_rating:
            qs = qs.filter(avg_rating__gte=min_rating)

        sort = params.get("sort", "")
        if sort in self.SORT_MAP:
            qs = qs.order_by(self.SORT_MAP.get(sort))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["audience_choices"] = Product.AUDIENCE_CHOICES
        context["categories"] = Category.objects.all()

        return context


class ProductDetailView(DetailView):
    template_name = "shop/product_detail.html"
    context_object_name = "product"
    model = Product

    # def get_queryset(self):
    #     return Product.objects.with_rating().select_related("category", "brand")

