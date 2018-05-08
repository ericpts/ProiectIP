from django import forms

from .models import ImageConversion


class ImageAddForm(forms.ModelForm):
    class Meta:
        model = ImageConversion
        fields = ('title', 'original_image')
