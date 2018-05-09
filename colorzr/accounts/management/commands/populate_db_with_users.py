from django.core.management.base import BaseCommand
from accounts.models import Profile
from django.contrib.auth.models import User
import json
from pathlib import Path
from random import randint

class Command(BaseCommand):
    help = 'Populate db with users'

    def _create_users(self, *args, **options):
        # load data
        users_str = (Path(__file__).resolve().parent.parent / 'data' / 'usernames.json').resolve() 
        first_names_str = (Path(__file__).resolve().parent.parent / 'data' / 'first_names.json').resolve()
        last_names_str = (Path(__file__).resolve().parent.parent / 'data' / 'last_names.json').resolve()

        with open(str(users_str), "r") as f:
            users_data = json.load(f)

        with open(str(first_names_str), "r") as f:
            first_names_data = json.load(f)

        with open(str(last_names_str), "r") as f:
            last_names_data = json.load(f)

        length = options['no_of_users'][0]

        # generate users
        for i in range(0, length):
            min_size = min(len(users_data), len(first_names_data), len(last_names_data))
            pos = randint(0, min_size - 1)
 
            try:
                User.objects.create_user(username=users_data[pos], 
                        password='gogo1234', 
                        first_name=first_names_data[pos],
                        last_name=last_names_data[pos])
            except Exception:
                print('Could not create user {}'.format(users_data[pos]))
            else:
                print('User created with username {}, password gogo1234, first name {} and last name {}'.format(users_data[pos], first_names_data[pos], last_names_data[pos]))

            # clear
            users_data.pop(pos)
            first_names_data.pop(pos)
            last_names_data.pop(pos)

    

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('no_of_users', nargs='+', type=int)

    def handle(self, *args, **options):
        self._create_users(*args, **options)
           