from django.views.generic import TemplateView

from images.models import ImageConversion

class HomeView(TemplateView):
    template_name = "index.html"

    # define context (aka bindings) for template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        current_user_savedImages = ImageConversion.objects.filter(author__exact=user) 
        context['images_list'] = current_user_savedImages
        return context