from django import forms

from .models import SavedImage

class ImageAddForm(forms.ModelForm):
    class Meta:
        model = SavedImage
        fields = ('title', 'original_image')
