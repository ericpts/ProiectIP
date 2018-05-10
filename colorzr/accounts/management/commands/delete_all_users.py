from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import json
from pathlib import Path
from random import randint

class Command(BaseCommand):
    help = 'Delete all users in db (and all their data)'

    def _delete_all_users(self, *args, **options):
        try:
            User.objects.all().delete()
            print('Successfully deleted all users')
        except Exception:
            print('Could not delete users')

    def handle(self, *args, **options):
        self._delete_all_users(*args, **options)
           