from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models

import PIL
from io import BytesIO

from .imgproc_mock import to_bw, to_color


class ImageConversion(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    bw_image = models.ImageField(upload_to='bw/')
    color_image = models.ImageField(upload_to='color/')
    original_image = models.ImageField(upload_to='original/')

    def __str__(self):
        return self.title

    @staticmethod
    def convert(image):
        original_image = PIL.Image.open(image)
        bw = to_bw(original_image)
        color = to_color(bw)

        def pil_to_model(img: PIL.Image):
            bio = BytesIO()
            img.save(bio, format='JPEG')
            return ContentFile(bio.getvalue())

        return pil_to_model(bw), pil_to_model(color)

    class Meta:
        ordering = ('created', )
