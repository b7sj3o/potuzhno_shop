from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")



class LoginForm(BootstrapMixin, AuthenticationForm):
    ...


class RegisterForm(BootstrapMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", )