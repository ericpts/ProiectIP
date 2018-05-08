from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from images.models import ImageConversion


class HomeView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("latest"))
        return super().dispatch(request, args, kwargs)
