from django.views.generic import TemplateView


class ReviewsHomeView(TemplateView):
    template_name = "reviews/home.html"

