from django.contrib.auth.models import User
from django.db import models


class ImageConversion(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    bw_image = models.ImageField(upload_to='bw/')
    color_image = models.ImageField(upload_to='color/')
    original_image = models.ImageField(upload_to='original/')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)
