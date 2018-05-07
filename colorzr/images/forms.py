from django import forms

from .models import SavedImage

class ImageAddForm(forms.ModelForm):
    uploaded_file = forms.ImageField(
        required=True
    )

    class Meta:
        model = SavedImage
        fields = ('title', 'original_image')
