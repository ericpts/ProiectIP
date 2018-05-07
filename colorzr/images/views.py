from django.shortcuts import render
from django.views import generic, View
from django.urls import reverse_lazy
from django.core.files.base import ContentFile


from images.models import SavedImage
from images.serializers import SavedImageSerializer
from rest_framework import mixins, generics

from . import forms
from .imgproc import to_bw, to_color

import uuid
import PIL


class ImageList(generics.ListCreateAPIView):
    queryset = SavedImage.objects.all()
    serializer_class = SavedImageSerializer


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavedImage.objects.all()
    serializer_class = SavedImageSerializer

class ImageAddView(generic.FormView):
    form_class = forms.ImageAddForm
    success_url = reverse_lazy('home')
    template_name = 'images/add_image.html'

    def form_valid(self, form):
        raw_image = PIL.Image.open(form.cleaned_data['uploaded_file'])
        title = form.cleaned_data['title']

        bw = to_bw(raw_image)
        color = to_color(bw)

        import pdb
        pdb.set_trace()

        # Save images with random filenames.
        name = str(uuid.uuid4()) + '.jpg'

        model_image = SavedImage()
        model_image.title = title
        model_image.bw_image.save(name, bw)
        model_image.color_image.save(name, color)

        model_image.save()
