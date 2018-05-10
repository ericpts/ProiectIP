from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from accounts.models import Profile, User
import json
from pathlib import Path
from random import randint, choice
import random
import os

class Command(BaseCommand):
    help = 'Populate db with profiles for users'

    def _create_profiles(self, *args, **options):
        # load data
        avatars_dir = (Path(__file__).resolve().parent.parent.parent.parent.parent / 'extern' / 'avatars' / 'dataset').resolve() 

        users = User.objects.all()

        for user in users:
            try:
                # delete the previous profile
                previous_profile = Profile.objects.filter(user = user)
                previous_profile.delete()

                # choose an avatar for it
                avatar_path = str(avatars_dir) + '/' + random.choice(os.listdir(str(avatars_dir)))

                # create bio 
                bio_str = 'My name is {} {}'.format(user.first_name, user.last_name)

                # create the profile record
                profile = Profile.objects.create(user=user)
                profile.bio = bio_str
                profile.avatar = ImageFile(open(avatar_path, "rb"))
                profile.save()

                print('Successfully created a new profile for user {}'.format(user))
            except Exception:
                print('Could not create new profile for user {}'.format(user))
           

    def handle(self, *args, **options):
        self._create_profiles(*args, **options)
           