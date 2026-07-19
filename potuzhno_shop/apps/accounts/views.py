from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from apps.shop.models import Product


class AccountsHomeView(TemplateView):
    template_name = "accounts/home.html"

class FavouriteToggleView(View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        profile = request.user.profile
        if product in profile.favourites.all():
            profile.favourites.remove(product)
        else:
            profile.favourites.add(product)
        return redirect('shop:product_detail', slug=slug)

class FavouritesView(TemplateView):
    template_name = "accounts/favourites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.request.user.profile.favourites.all()
        return context