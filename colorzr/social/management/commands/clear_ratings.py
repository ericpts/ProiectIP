from django.core.management.base import BaseCommand
from images.models import ImageConversion
from social.models import Rating
from accounts.models import User
import json
from pathlib import Path
from random import randint, choice
import random
import os

class Command(BaseCommand):
    def _create_ratings(self, *args, **options):
        try:
            Rating.objects.all().delete()
            print('Deleted all ratings in db')
        except Exception as e:
            print('Could not delete raings')
            print(e)    

    def handle(self, *args, **options):
        self._create_ratings(*args, **options)
           