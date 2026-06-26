from django.http import  Http404
from django.views.generic import TemplateView, ListView, DetailView

PRODUCTS = [
    {"id": 1, "name": "Худі Oversize", "brand": "ПОТУЖНО", "price": 1290, "sizes": ["S", "M", "L"]},
    {"id": 2, "name": "Кросівки Runner", "brand": "Nova", "price": 2490, "sizes": ["40", "41", "42"]},
    {"id": 3, "name": "Футболка Basic", "brand": "ПОТУЖНО", "price": 590, "sizes": ["XS", "S", "M", "L"]},
    {"id": 4, "name": "Футболка Basic", "brand": "ПОТУЖНО", "price": 590, "sizes": ["XS", "S", "M", "L"]},
]


class HomeView(TemplateView):
    template_name = "shop/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured"] = PRODUCTS[:3]

        return context


class ProductListView(ListView):
    template_name = "shop/product_list.html"
    context_object_name = "products"

    # TODO: змінити коли добавляться моделі
    def get_queryset(self):
        return PRODUCTS



class ProductDetailView(DetailView):
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    # TODO: змінити коли добавляться моделі
    def get_object(self, queryset=None):
        product = next((p for p in PRODUCTS if p['id'] == self.kwargs.get("pk", 0)), None)

        if product is None:
            raise Http404()

        return product

