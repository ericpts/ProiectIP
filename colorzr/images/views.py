from io import BytesIO

from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages


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
    template_name = 'images/upload-image.html'

    def get(self, request, *args, **kwargs):
        image_form = forms.ImageAddForm({}) # no need for validation so formView is unbound
        return render(request, self.template_name, { 'image_form': image_form })

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

        model_image = SavedImage()
        model_image.title = title
        model_image.original_image.save(name, form.cleaned_data['original_image'])
        model_image.bw_image.save(name, pil_to_model(bw))
        model_image.color_image.save(name, pil_to_model(color))

        model_image.save()

        # return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        image_form = forms.ImageAddForm(request.POST, request.FILES) # need validation so formView is bound to ImageAddView model
        
        if image_form.is_valid():
            self.form_valid(image_form)
            messages.success(request, 'You successfully uploaded your image!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('home')
