from django import forms

from .models import *


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
