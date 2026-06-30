from django.views.generic import TemplateView


class OrdersHomeView(TemplateView):
    template_name = "orders/home.html"

