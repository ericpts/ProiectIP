from rest_framework import serializers
from images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'title', 'base64_bw', 'base64_color')

