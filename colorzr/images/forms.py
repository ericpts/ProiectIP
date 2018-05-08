from django import forms

from .models import ImageConversion
from social.models import Comment


class ImageAddForm(forms.ModelForm):
    class Meta:
        model = ImageConversion
        fields = ('title', 'original_image')


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        labels = {
            "text": "Comment"
        }