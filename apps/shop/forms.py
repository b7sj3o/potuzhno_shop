from django import forms
from django.utils.text import slugify
from .models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name", "category", "brand", "description",
            "price", "is_active", "is_featured", "sku",
            "audience", "stock", "sizes"
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "sizes": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data:
            data = self.data.copy()
            name = data.get("name", "")
            data["slug"] = slugify(name)
            self.data = data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "text")
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Ваш відгук..."}),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text", "")
        rating = self.cleaned_data.get("rating", 5)

        if rating <= 2 and len(text.strip()) < 5:
            raise forms.ValidationError("Якщо оцінка 2 або менше, відгук має містити щонайменше 5 символів.")
        return text
