from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class LoggedInTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@test.com', 'password123')
        self.client = Client()
        self.client.login(username='admin', password='password123')

    def test_home_page_redirect(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('latest'))