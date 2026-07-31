from django.contrib import messages
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, Review
from .forms import ProductFilterForm, ContactForm, ProductForm, ReviewForm, unique_slug


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

        self.filter_form = ProductFilterForm(self.request.GET or None)

        if not self.filter_form.is_valid():
            return qs

        data = self.filter_form.cleaned_data

        if data.get("q"):
            qs = qs.filter(
                Q(name__icontains=data["q"])
                | Q(brand__name__icontains=data["q"])
                | Q(category__name__icontains=data["q"])
            )
        if data.get("category"):
            qs = qs.filter(category=data["category"])
        if data.get("audience"):
            qs = qs.filter(audience=data["audience"])
        if data.get("min_price"):
            qs = qs.filter(price__gte=data["min_price"])
        if data.get("max_price"):
            qs = qs.filter(price__lte=data["max_price"])
        if data.get("min_rating"):
            qs = qs.filter(avg_rating__gte=data["min_rating"])

        if data.get("sort") in self.SORT_MAP:
            qs = qs.order_by(self.SORT_MAP.get(data["sort"]))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filter_form"] = self.filter_form

        return context


class ProductDetailView(DetailView):
    template_name = "shop/product_detail.html"
    context_object_name = "product"
    model = Product

    def get_queryset(self):
        return Product.objects.with_rating()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["review_form"] = ReviewForm()

        return context



@login_required
def toggle_favourite(request, slug):
    user_profile = request.user.profile
    product = get_object_or_404(Product, slug=slug)
    if user_profile.favourites.filter(pk=product.pk).exists():
        user_profile.favourites.remove(product)
    else:
        user_profile.favourites.add(product)
    return redirect("shop:product_detail", slug=slug)


class FavouriteListView(LoginRequiredMixin, ProductListView):
    def get_queryset(self):
        return super().get_queryset().filter(
            favourited_by=self.request.user.profile
        )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            print(f"[CONTACT] {data['name']} <{data['email']}> "
                  f"[{data['subject']}] #{data['order_number'] or '—'}: {data['message']}")

            messages.success(request, "Форма було успішно надіслана!")
            return redirect(f"{reverse('shop:contact')}")
    else:
        form = ContactForm()

    return render(request, "shop/contact.html", {"form": form})


@login_required
def review_create(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ReviewForm(request.POST)

    if request.method == "POST":
        if Review.objects.filter(user=request.user, product=product).count() > 0:
            messages.error(request, "Ви вже написали відгук для цього продукту")
            return redirect("shop:product_detail", slug=product.slug)

        form.instance.product = product
        form.instance.user = request.user

        if form.is_valid():
            form.save()

            messages.success(request, "Відгук був успішно створений")
            return redirect("shop:product_detail", slug=product.slug)

        # TODO: добавити утиліту або декоратор для показу помилок замість цього:
        for error in form.errors.values():
            messages.error(request, "\n".join(error))


    return render(request, "shop/product_detail.html", {
        "product": product,
        "review_form": form
    })


@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    messages.success(request, "Відгук був успішно видалений")

    return redirect("shop:product_detail", slug=review.product.slug)

def product_create(request):
    form = ProductForm(request.POST or None)

    if request.method == "POST":
        form.instance.slug = unique_slug(request.POST.get("name", ""))

        if form.is_valid():
            product = form.save()
            messages.success(request, f'Продукт "{product.name}" був успішно створений')
            return redirect("shop:product_detail", slug=product.slug)
        messages.error(request, "Трапилась помилка")


    return render(request, "shop/product_form.html", {"form": form})


def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, instance=product)

    if request.method == "POST":
        form.instance.slug = unique_slug(request.POST.get("name", ""), instance=product)

        if form.is_valid():
            product = form.save()
            messages.success(request, f'Продукт "{product.name}" був успішно оновлений')
            return redirect("shop:product_detail", slug=product.slug)
        messages.error(request, "Трапилась помилка")


    return render(request, "shop/product_form.html", {"form": form, "product": product})

