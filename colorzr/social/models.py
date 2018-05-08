
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

import PIL
from io import BytesIO

from django.db.models import Avg

from images.models import ImageConversion


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
