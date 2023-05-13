from django.urls import reverse

from task_manager.users.models import CustomUser
from django.test import TestCase, Client
from http import HTTPStatus


# Create your tests here.

class UsersTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('users_create')
        self.login_url = reverse('users_login')
        self.home = reverse('home')
        self.username = 'vadsa'
        self.password = 'testpass123'
        self.user_data = {
            'username': self.username,
            'first_name': 'Ivan',
            'last_name': 'Petrov',
            'password1': self.password,
            'password2': self.password,
        }

    def test_user_registration(self):
        response = self.client.post(self.signup_url, data=self.user_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, self.login_url)
        print(CustomUser.objects.last())

    def test_user_login(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # self.assertTrue('_auth_user_id' in self.client.session)
        # self.assertRedirects(response, self.home)
