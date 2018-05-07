import uuid
from io import BytesIO

import PIL
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics

from .serializers import ImageConversionSerializer
from .models import ImageConversion
from . import forms
from .imgproc_mock import to_bw, to_color


class ImageList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = ImageConversion.objects.all()
    serializer_class = ImageConversionSerializer


class ImageDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ImageConversion.objects.all()
    serializer_class = ImageConversionSerializer


class ImageAddView(LoginRequiredMixin, generic.FormView):
    form_class = forms.ImageAddForm
    success_url = reverse_lazy('home')
    template_name = 'images/upload-image.html'

    def form_valid(self, form):
        original_image = PIL.Image.open(form.cleaned_data['original_image'])
        title = form.cleaned_data['title']

        bw = to_bw(original_image)
        color = to_color(bw)

        # Save images with random filenames.
        name = str(uuid.uuid4()) + '.jpg'

        def pil_to_model(img: PIL.Image):
            bio = BytesIO()
            img.save(bio, format='JPEG')
            return ContentFile(bio.getvalue())

        model_image = ImageConversion()

        model_image.title = title
        model_image.author = self.request.user
        model_image.original_image.save(name, form.cleaned_data['original_image'])
        model_image.bw_image.save(name, pil_to_model(bw))
        model_image.color_image.save(name, pil_to_model(color))

        model_image.save()

        return super().form_valid(form)