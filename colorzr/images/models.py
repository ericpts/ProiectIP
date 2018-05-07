from django.db import models
from PIL import Image


class SavedImage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)

    bw_image = models.ImageField(upload_to='bw/')
    color_image = models.ImageField(upload_to='color/')
    original_image = models.ImageField(upload_to='original/')

    class Meta:
        ordering = ('created',)
