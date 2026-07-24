from django import forms

from .models import Category, Product


class ProductFilterForm(forms.Form):
    SORT_CHOICES = [
        ("", "Новинки"),
        ("price", "Дешевші спершу"),
        ("-price", "Дорожчі спершу"),
        ("name", "За назвою (А–Я)"),
        ("-avg_rating", "За рейтингом"),
    ]
    RATING_CHOICES = [("", "Будь-який"), ("4", "4★ і вище"), ("3", "3★ і вище")]

    q = forms.CharField(
        required=False, label="Пошук за назвою",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "напр. худі"
        })
    )
    category = forms.ModelChoiceField(
        required=False, label="Категорія", queryset=Category.objects.all(), empty_label="Усі",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    audience = forms.ChoiceField(
        required=False, label="Категорія",
        choices=[("", "Будь-яка")] + Product.AUDIENCE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    min_price = forms.DecimalField(
        required=False, min_value=0, label="Ціна від",
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "від"}),
    )
    max_price = forms.DecimalField(
        required=False, min_value=0, label="Ціна до",
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "до"}),
    )
    min_rating = forms.ChoiceField(
        required=False, label="Рейтинг", choices=RATING_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    sort = forms.ChoiceField(
        required=False, label="Сортування", choices=SORT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def clean(self):
        cleaned = super().clean()
        mn, mx = cleaned.get("min_price"), cleaned.get("max_price")
        if mn is not None and mx is not None and mn > mx:
            raise forms.ValidationError("Ціна «від» не може бути більшою за «до».")
        return cleaned


class ContactForm(forms.Form):
    SUBJECT_CHOICES = [
        ("product", "Питання про товар"),
        ("order", "Питання про замовлення"),
        ("delivery", "Доставка й оплата"),
        ("return", "Повернення / обмін"),
        ("other", "Інше"),
    ]

    name = forms.CharField(
        label="Ваше ім'я", max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Як до вас звертатися"}),
    )
    email = forms.EmailField(
        label="Email", help_text="Сюди надішлемо відповідь.",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
    )
    subject = forms.ChoiceField(
        label="Тема звернення", choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    order_number = forms.CharField(
        label="Номер замовлення", max_length=20, required=False,
        help_text="Обов'язково для тем про замовлення чи повернення.",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "напр. 100237"}),
    )
    message = forms.CharField(
        label="Повідомлення", min_length=10,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5,
                                     "placeholder": "Опишіть питання якомога детальніше"}),
    )
    consent = forms.BooleanField(
        label="Погоджуюсь на обробку персональних даних",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Повідомлення надто коротке — опишіть детальніше (мін. 10 символів).")
        return message

    def clean(self):
        cleaned = super().clean()
        subject = cleaned.get("subject")
        order_number = cleaned.get("order_number")
        if subject in ("order", "return") and not order_number:
            # add_error прив'язує помилку до конкретного поля (а не до всієї форми)
            self.add_error("order_number", "Для цієї теми вкажіть номер замовлення.")
        return cleaned

