from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView as DjangoLoginView

from .forms import LoginForm, RegisterForm


class AccountsHomeView(TemplateView):
    template_name = "accounts/home.html"


# def login_view(request):
#     form = LoginForm(request, data=request.POST or None)
#
#     if request.method == "POST" and form.is_valid():
#         user = form.get_user()
#         login(request, user)
#
#         messages.success(request, "Ви успішно увійшли в акаунт!")
#
#         next_url = request.POST.get("next")
#         if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
#             return redirect(next_url)
#
#         return redirect("shop:home")
#
#
#     return render(request, "accounts/login.html", {
#         "form": form,
#         "next": request.GET.get("next", "")
#     })
#

class LoginView(DjangoLoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

def register(request):
    form = RegisterForm(data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)

        messages.success(request, "Ви успішно створили акаунт!")

        return redirect("shop:home")

    return render(request, "accounts/register.html", {
        "form": form,
    })

#
# def logout_view(request):
#     if request.method == "POST":
#         logout(request)
#         messages.success(request, "Ви успішно вийшли з акаунту!")
#
#     return redirect("shop:home")


@login_required
def profile(request):
    return render(request, "accounts/profile.html", {
        "favourites": request.user.profile.favourites.all(),
        "reviews": request.user.reviews.select_related("product")
    })