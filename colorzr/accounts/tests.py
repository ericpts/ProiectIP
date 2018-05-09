from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from friendship.models import Follow

from .models import Profile


class DatabaseTestCase(TestCase):
    def setUp(self):
        self.adam = User.objects.create_user('Adam', 'admin@test.com', 'password123')
        self.bob = User.objects.create_user('Bob', 'bob@yahoo.com', 'password123')
        self.charlie = User.objects.create_user('Charlie', 'charlie@yahoo.com', 'password123')

        Follow.objects.add_follower(self.adam, self.bob)
        Follow.objects.add_follower(self.adam, self.charlie)
        Follow.objects.add_follower(self.bob, self.charlie)

        self.client = Client()

    def test_profile_created(self):
        self.assertTrue(Profile.objects.filter(user__username='Adam').exists(),
                        'Profile should be created for each user')
        self.assertFalse(Profile.objects.filter(user__username='does_not_exist').exists(),
                         'User not added, so profile should not exist')

    def test_follower_count(self):
        self.assertEqual(self.adam.profile.follower_count(), 0)
        self.assertEqual(self.bob.profile.follower_count(), 1)
        self.assertEqual(self.charlie.profile.follower_count(), 2)

        self.assertIn(self.adam, Follow.objects.followers(self.charlie))
        self.assertIn(self.charlie, Follow.objects.following(self.bob))


class LoggedOutTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@test.com', 'password123')
        self.client = Client()

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






