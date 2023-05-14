from django.contrib.messages import get_messages
from django.urls import reverse

from task_manager.users.models import CustomUser
from django.test import TestCase, Client
from http import HTTPStatus


class UsersTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('users_create')
        self.login_url = reverse('users_login')
        self.logout_url = reverse('logout')
        self.home = reverse('home')
        self.user_home = reverse('users_home')
        self.username = 'test'
        self.password = 'testpass123'
        self.user_data = {
            'username': self.username,
            'first_name': 'Ivan',
            'last_name': 'Petrov',
            'password1': self.password,
            'password2': self.password,
        }

        self.user_data2 = {
            'username': self.username,
            'password': self.password,
        }

        self.user1 = CustomUser.objects.get(pk=1)
        self.user2 = CustomUser.objects.get(pk=2)

    def test_user_registration(self):
        response = self.client.post(self.signup_url, data=self.user_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, self.login_url)

    def test_user_login_and_logout(self):
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)
        response = self.client.post(self.login_url, data=self.user_data2)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.home)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.home)

    def test_home(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.home)
        self.assertContains(response, f'Привет {self.user1.username}')

    def test_update(self):
        self.client.force_login(self.user1)
        url = reverse('users_update', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        updated_user = CustomUser.objects.get(id=self.user1.id)
        self.assertEqual(updated_user.first_name, 'Ivan')
        self.assertEqual(updated_user.last_name, 'Petrov')

    def test_delete(self):
        self.client.force_login(self.user1)
        url = reverse('users_delete', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=self.user1.id)

    def test_user_no_permission_delete_page(self):
        client = Client(HTTP_REFERER=self.user_home,)
        client.force_login(self.user1)
        url = reverse('users_delete', args=[self.user2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        messages = list(get_messages(response.wsgi_request))[0]
        self.assertEqual(str(messages), 'У вас нет прав для изменения другого пользователя.')
