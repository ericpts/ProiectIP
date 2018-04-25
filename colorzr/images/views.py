from django.shortcuts import render

from images.models import Image
from images.serializers import ImageSerializer
from rest_framework import mixins, generics


class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
