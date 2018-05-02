from pathlib import Path

from django.db import models
from django.contrib.auth.models import User


def get_image_path(instance, filename: str) -> str:
    return str(Path('photos') / str(instance.id) / filename)


class Image(models.Model):
    user = models.OneToOneField(User)
    image = ImageField(upload_to=get_image_path, blank=True, null=True)
