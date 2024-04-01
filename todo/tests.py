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

    def test_todo_create(self):
        url = reverse('todo:todo-create')
        self.client.force_login(self.user)

        data = {
            'title': 'Test Todo',
            'completed': False
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title='Test Todo').exists())

    def test_todo_list(self):
        url = reverse('todo:todo-list')
        self.client.force_login(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_detail(self):
        todo = Task.objects.create(title='Test Todo', completed=False, created_by=self.user)
        url = reverse('todo:todo-detail', args=[Task.id])
        self.client.force_login(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_update(self):
        todo = Task.objects.create(title='Test Todo', completed=False, created_by=self.user)
        url = reverse('todo:todo-update', args=[Task.id])
        self.client.force_login(self.user)

        data = {
            'title': 'Updated Todo',
            'completed': True
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Task.objects.filter(title='Updated Todo').exists())

    def test_todo_delete(self):
        todo = Task.objects.create(title='Test Todo', completed=False, created_by=self.user)
        url = reverse('todo:todo-delete', args=[Task.id])
        self.client.force_login(self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(title='Test Todo').exists())
