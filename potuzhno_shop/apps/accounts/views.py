from django.views.generic import TemplateView


class AccountsHomeView(TemplateView):
    template_name = "accounts/home.html"

