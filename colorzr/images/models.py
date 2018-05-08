from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

import PIL
from io import BytesIO

from django.db.models import Avg

from .imgproc_mock import to_bw, to_color


class ImageConversion(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    bw_image = models.ImageField(upload_to='bw/')
    color_image = models.ImageField(upload_to='color/')
    original_image = models.ImageField(upload_to='original/')

    def __str__(self):
        return "{0}'s \"{1}\"".format(self.author, self.title)

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

    def get_mean_rating(self):
        if self.rating_set.count() == 0:
            return 0
        return self.rating_set.aggregate(Avg('rating'))['rating__avg']


class Rating(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(ImageConversion, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('author', 'image'),)

    def __str__(self):
        return "{0}* rating to {1}'s {2}".format(self.rating, self.image.author, self.image.title)


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(ImageConversion, on_delete=models.CASCADE)
    text = models.TextField(max_length=1024)

    def __str__(self):
        return "[{0}]: {1}".format(self.author, self.text)
