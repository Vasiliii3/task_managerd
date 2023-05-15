from django.contrib.messages import get_messages
from django.urls import reverse
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from django.test import TestCase, Client
from http import HTTPStatus
from task_manager.tasks.filters import TaskFilter


class TaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        self.home = reverse('tasks_home')
        self.client = Client(HTTP_REFERER=self.home, )
        self.user1 = CustomUser.objects.get(pk=1)
        self.user2 = CustomUser.objects.get(pk=2)
        self.client.force_login(self.user1)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.new_task = reverse('tasks_creaate')
        self.login_url = reverse('users_login')
        self.name = 'Корова кушает траву'
        self.description = 'Му му'
        self.task_data = {
            "name": self.name,
            "description": self.description,
            "status": self.status1.id,
            "author": self.user1.id,
            "executor": self.user2.id,
        }

    def test_task_access_page(self):
        response = self.client.get(self.home)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.client.logout()
        response = self.client.get(self.home)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_url)

    def test_task_creature(self):
        response = self.client.post(self.new_task, data=self.task_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        test_task = Task.objects.last()
        self.assertEqual(test_task.name, self.name)

    def test_curent_view(self):
        url = reverse('tasks_current', args=[self.task2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task2.name)

    def test_curent_view_returns_404_for_invalid_object_id(self):
        url = reverse('tasks_current', args=[99])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_task_update(self):
        url = reverse('tasks_update', args=[self.task2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = {
            "name": self.name,
            "description": self.description,
            "status": 2,
            "author": 1,
            "executor": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        updated_taks = Task.objects.get(id=self.task2.id)
        self.assertEqual(updated_taks.name, self.name)
        self.assertEqual(updated_taks.description, self.description)

    def test_task_delete(self):
        url = reverse('tasks_delete', args=[self.task2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task2.id)

    def test_task_no_authoes_delete_page(self):
        url = reverse('tasks_delete', args=[self.task1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        messages = list(get_messages(response.wsgi_request))[0]
        self.assertEqual(str(messages), 'Задачу может удалить только её автор')

    def test_filter_by_is_author_true(self):
        filter = TaskFilter({'is_author': 'true'}, queryset=Task.objects.all(),
                            request=self.client.request().wsgi_request)
        filtered_qs = filter.qs
        self.assertIn(self.task2, filtered_qs)
        self.assertNotIn(self.task1, filtered_qs)

    def test_filter_by_status(self):
        filter = TaskFilter({'status': self.status1.id}, queryset=Task.objects.all(),
                            request=self.client.request().wsgi_request)
        filtered_qs = filter.qs
        self.assertIn(self.task1, filtered_qs)
        self.assertNotIn(self.task2, filtered_qs)

    def test_filter_by_executor(self):
        filter = TaskFilter({'executor': self.user2.id}, queryset=Task.objects.all(),
                            request=self.client.request().wsgi_request)
        filtered_qs = filter.qs
        self.assertIn(self.task3, filtered_qs)
        self.assertNotIn(self.task2, filtered_qs)
