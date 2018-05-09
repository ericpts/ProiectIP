from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib import auth

from .models import Profile


class LoggedOutTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@test.com', 'password123')
        self.client = Client()

    def test_profile_created(self):
        self.assertTrue(Profile.objects.filter(user__username='admin').exists(),
                        'Profile should be created for each user')
        self.assertFalse(Profile.objects.filter(user__username='does_not_exist').exists(),
                         'User not added, so profile should not exist')

    def test_account_login_logout(self):
        self.client.post(reverse('login'), {'username': 'admin', 'password': 'password123'})
        self.assertTrue(auth.get_user(self.client).is_authenticated,
                        "User should be authenticated")
        self.client.post(reverse('logout'), {})
        self.assertFalse(auth.get_user(self.client).is_authenticated,
                         "User should not be authenticated")


class LoggedInTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@test.com', 'password123')
        self.client = Client()
        self.client.login(username='admin', password='password123')

    def test_homepage_redirect(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)







