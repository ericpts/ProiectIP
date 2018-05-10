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
    help = 'Populate db with ratings'

    def _create_ratings(self, *args, **options):
        users = User.objects.all()
        images = ImageConversion.objects.all()
        no_of_ratings = options['no_of_ratings'][0]

        for i in range(0, no_of_ratings):
            # take a random user
            user = random.choice(users)

            # take a random upload
            image = random.choice(images)

            try:
                # delete the previous rating if it exists
                previous_rating = Rating.objects.filter(author=user, image=image)
                previous_rating.delete()

                # create rating record
                rating = Rating(author=user, image=image, rating=randint(1, 5))
                rating.save()

                print('Successfully created rating by {} for upload {} of user {}'.format(user, image.title, image.author))
                
            except Exception as e:
                print('Could not rate the upload with title {} of user {}'.format(image.title, image.author))
                print(e)           
    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('no_of_ratings', nargs='+', type=int)

    def handle(self, *args, **options):
        self._create_ratings(*args, **options)
           