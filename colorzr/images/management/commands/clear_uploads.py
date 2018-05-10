from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from django.core.files import File
from accounts.models import User
from images.models import ImageConversion
import json
from pathlib import Path
from random import randint, choice
import random
import os

class Command(BaseCommand):
    def _delete_uploads(self, *args, **options):
        try:
            ImageConversion.objects.all().delete()
            print('Deleted all image uploads in db')
        except Exception as e:
            print('Could not delete uploads')
            print(e)

    def handle(self, *args, **options):
        self._delete_uploads(*args, **options)
           