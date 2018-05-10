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
    help = 'Populate db with comments'

    def _create_comments(self, *args, **options):
        # load data
        fake_news_path = (Path(__file__).resolve().parent.parent / 'data' / 'fake_news.csv').resolve() 

        csv.field_size_limit(sys.maxsize)
        no_of_commnets = options['no_of_comments'][0]
        fake_news_dict = csv.DictReader(open(str(fake_news_path)))
        fake_news_list = []
        for row in fake_news_dict:
            if len(row['title']) < 1000 and len(row['text']) < 1000:
                fake_news_list.append(row)
        
        users = User.objects.all()
        images = ImageConversion.objects.all()

        for i in range(0, no_of_commnets):
             # take a random user
            user = random.choice(users)

            # take a random upload
            image = random.choice(images)

            try:
                # take a random comment
                pos = randint(0, len(fake_news_list) - 1)
                comment_str = fake_news_list[pos]['title']
                fake_news_list.pop(pos)

                # create a record
                comment = Comment(author=user, image=image, text=comment_str)
                comment.save()

                print('Successfully created {}\'s comment for upload {} of user {}'.format(user, image.title, image.author))

            except Exception as e:
                print('Could not create {}\'s comment for upload {} of user {}'.format(user, image.title, image.author))
                print(e)

    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('no_of_comments', nargs='+', type=int)

    def handle(self, *args, **options):
        self._create_comments(*args, **options)
           