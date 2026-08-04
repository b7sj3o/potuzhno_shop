from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Product
from .serializers import ProductSerializer
from .services.product_service import soft_delete_product, restore_product
from .forms import ProductForm

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock']

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        soft_delete_product(self.get_object())
        return Response({'status': 'product soft deleted'})

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        product = Product.all_objects.get(pk=pk)
        restore_product(product)
        return Response({'status': 'product restored'})


def form_errors_to_messages(request, form):
    """Утиліта для виведення помилок форми через Django messages"""
    for field, errors in form.errors.items():
        for error in errors:
            field_label = form.fields[field].label if field in form.fields and form.fields[field].label else field
            messages.error(request, f"Помилка у полі '{field_label}': {error}")


class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/product_form.html"
    success_url = reverse_lazy("shop:product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.stock == 0:
            messages.warning(self.request, "Товар додано, але його немає в наявності.")
        else:
            messages.success(self.request, "Товар успішно створено!")
        return response


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/product_form.html"

    def get_success_url(self):
        return reverse_lazy("shop:product_detail", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.stock == 0:
            messages.warning(self.request, "Товар оновлено, але його немає в наявності.")
        else:
            messages.success(self.request, "Товар успішно оновлено!")
        return response


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "shop/product_confirm_delete.html"
    success_url = reverse_lazy("shop:product_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Товар успішно видалено!")
        return super().delete(request, *args, **kwargs)
