from django.urls import reverse
from task_manager.users.models import CustomUser
from task_manager.labels.models import Label
from django.test import TestCase, Client
from http import HTTPStatus


class LabelsTest(TestCase):
    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        self.client = Client()
        self.user1 = CustomUser.objects.get(pk=1)
        self.client.force_login(self.user1)
        self.label1 = Label.objects.get(pk=1)
        self.home = reverse('lablels_home')
        self.new_label = reverse('lablels_creaate')
        self.login_url = reverse('users_login')
        self.name = 'меткатеста'
        self.label_data = {
            'name': self.name,
        }

    def test_lables_access_page(self):
        response = self.client.get(self.home)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.client.logout()
        response = self.client.get(self.home)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_url)

    def test_lables_creature(self):
        response = self.client.post(self.new_label, data=self.label_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        test_labels = Label.objects.last()
        self.assertEqual(test_labels.name, self.name)

    def test_lables_update(self):
        url = reverse('lablels_update', args=[self.label1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(url, self.label_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        updated_label = Label.objects.get(id=self.label1.id)
        self.assertEqual(updated_label.name, self.name)

    def test_lables_delete(self):
        url = reverse('lablels_delete', args=[self.label1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(url, self.label_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(id=self.label1.id)
