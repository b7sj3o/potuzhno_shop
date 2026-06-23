from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

PRODUCTS = [
    {"id": 1, "name": "Худі Oversize", "brand": "ПОТУЖНО", "price": 1290, "sizes": ["S", "M", "L"]},
    {"id": 2, "name": "Кросівки Runner", "brand": "Nova", "price": 2490, "sizes": ["40", "41", "42"]},
    {"id": 3, "name": "Футболка Basic", "brand": "ПОТУЖНО", "price": 590, "sizes": ["XS", "S", "M", "L"]},
    {"id": 4, "name": "Футболка Basic", "brand": "ПОТУЖНО", "price": 590, "sizes": ["XS", "S", "M", "L"]},
]


class HomeView(View):
    def get(self, request, *args, **kwargs):
        print(kwargs)
        return HttpResponse(""
                            "<b>Привіт, це магазин Potuzhno Shop</b>"
                            "<br /><p><a href='/products/'>До каталогу</a></p>"
                            )


class ProductListView(ListView):
    # TODO: змінити коли добавляться моделі
    def get_queryset(self):
        return PRODUCTS

    # TODO: змінити коли добавляться моделі
    def get(self, request, *args, **kwargs):
        response = ""
        for product in PRODUCTS:
            response += f"<li><a href=\"/products/{product['id']}\">{product['name']}</a></li>\n"

        return HttpResponse(f"<ul>{response}</ul>")


class ProductDetailView(DetailView):
    # TODO: змінити коли добавляться моделі
    def get_object(self, queryset=None):
        product = next((p for p in PRODUCTS if p['id'] == self.kwargs.get("pk", 0)), None)

        if product is None:
            raise Http404()

        return product

    # TODO: змінити коли добавляться моделі
    def get(self, request, *args, **kwargs):
        product = self.get_object()

        return HttpResponse(
            f"<h1>{product['name']}</h1>"
            f"<p>Бренд: {product['brand']}</p>"
            f"<p>Ціна: {product['price']} грн</p>"
            f"<p>Розміри: {', '.join(product['sizes'])}</p>"
            f'<p><a href="/products/">← до каталогу</a></p>'
        )

