from django.views.generic import TemplateView

from images.models import ImageConversion


class HomeView(TemplateView):
    template_name = "index.html"
