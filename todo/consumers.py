from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Task

class TodoViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_task_create(self):
        url = reverse('todo:task-create')  # Updated URL pattern name
        self.client.force_login(self.user)

        data = {
            'title': 'Test Task',
            'completed': False
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title='Test Task').exists())

    def test_task_list(self):
        url = reverse('todo:task-list')  # Updated URL pattern name
        self.client.force_login(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_detail(self):
        task = Task.objects.create(title='Test Task', completed=False)
        url = reverse('todo:task-detail', args=[task.pk])  # Updated URL pattern name
        self.client.force_login(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_update(self):
        task = Task.objects.create(title='Test Task', completed=False)
        url = reverse('todo:task-update', args=[task.pk])  # Updated URL pattern name
        self.client.force_login(self.user)

        data = {
            'title': 'Updated Task',
            'completed': True
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(pk=task.pk).title, 'Updated Task')

    def test_task_delete(self):
        task = Task.objects.create(title='Test Task', completed=False)
        url = reverse('todo:task-delete', args=[task.pk])  # Updated URL pattern name
        self.client.force_login(self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
