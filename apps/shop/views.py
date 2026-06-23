from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404

# Create your views here.
PRODUCTS = [
    {"id": 1, "name": "Худі Oversize", "brand": "ПОТУЖНО", "price": 1290, "sizes": ["S", "M", "L"], "image": "shop/img/hoody.jpg"},
    {"id": 2, "name": "Кросівки Runner", "brand": "Nova", "price": 2490, "sizes": ["40", "41", "42"]},
    {"id": 3, "name": "Футболка Basic", "brand": "ПОТУЖНО", "price": 590, "sizes": ["XS", "S", "M", "L"]},
    {"id": 4, "name": "Футболка Basic", "brand": "ПОТУЖНО", "price": 590, "sizes": ["XS", "S", "M", "L"]},
]

def home(request: HttpRequest):
    return HttpResponse("<b>Привіт, це магазин Potuzhno Shop</b><br /><p><a href='/products/'>До каталогу</a></p>")


def product_list(request: HttpRequest):
    response = ""
    for product in PRODUCTS:
        response += f"<li><a href=\"/products/{product['id']}\">{product['name']}</a></li>\n"

    return render(request, "shop/product_list.html", {"products": PRODUCTS})


def product_detail(request: HttpRequest, pk: int):
    product = next((p for p in PRODUCTS if p['id'] == pk), None)

    if product is None:
        raise Http404()
        # return render(request, '404.html')

    return render(request, "shop/product_detail.html", {"product": product})