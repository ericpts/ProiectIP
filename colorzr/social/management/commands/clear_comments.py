from django.core.management.base import BaseCommand
from accounts.models import User
from images.models import ImageConversion
from social.models import Comment
import json
from pathlib import Path
from random import randint, choice
import random
import os
import csv
import sys

class Command(BaseCommand):
    def _create_profiles(self, *args, **options):
        try:
            Comment.objects.all().delete()
            print('Deleted all comments in db')
        except Exception as e:
            print('Could not delete commnets')
            print(e)

    def handle(self, *args, **options):
        self._create_profiles(*args, **options)
           