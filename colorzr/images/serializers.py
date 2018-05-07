from rest_framework import serializers
from images.models import SavedImage

class SavedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedImage
        fields = ('id', 'created', 'title', 'bw_image', 'color_image')

