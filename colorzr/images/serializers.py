from rest_framework import serializers
from .models import ImageConversion


class ImageConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageConversion
        fields = ('id', 'created', 'author', 'title', 'bw_image', 'color_image')

