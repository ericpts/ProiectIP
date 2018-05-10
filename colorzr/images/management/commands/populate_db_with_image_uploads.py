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
    help = 'Populate db with profiles for users'

    def _create_profiles(self, *args, **options):
        # load data
        images_dir = (Path(__file__).resolve().parent.parent.parent.parent.parent / 'extern' / 'images' / 'dataset').resolve() 
        books_str = (Path(__file__).resolve().parent.parent / 'data' / 'books.json').resolve()

        with open(str(books_str), "r") as f:
            books_data = json.load(f)

        users = User.objects.all()
        no_of_uploads = options['no_of_image_uploads'][0]

        for i in range(0, no_of_uploads):
            # take a random user
            user = random.choice(users)

            try:
                # choose an image for it
                image_path = str(images_dir) + '/' + random.choice(os.listdir(str(images_dir)))
                bw, color = ImageConversion.convert(image_path)

                # choose title
                pos = randint(0, len(books_data) - 1)
                title = books_data[pos]['title']

                # create the record
                image_conversion = ImageConversion(author=user)
                image_conversion.title = title
                image_conversion.bw_image.save(str(random.choice(os.listdir(str(images_dir)))), bw, save=False)
                image_conversion.color_image.save(str(random.choice(os.listdir(str(images_dir)))), color, save=False)
                image_conversion.original_image.save(str(random.choice(os.listdir(str(images_dir)))), File(open(image_path, 'rb')), save=False)
                image_conversion.save()

                print('Successfully uploaded image {} for user {} with title {}'.format(image_path, user, title))
            except Exception as e:
                print('Could not upload for user {}'.format(user))
                print(e)           
    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('no_of_image_uploads', nargs='+', type=int)

    def handle(self, *args, **options):
        self._create_profiles(*args, **options)
           