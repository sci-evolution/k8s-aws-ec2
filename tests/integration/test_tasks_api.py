import json
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from django.test import TestCase, Client
from django.urls import reverse
from tasks.models import Task


class TaskAPITests(TestCase):
    """
    Integration tests for the Task API endpoints.
    """
    def setUp(self):
        """
        Set up test data and client for API tests.

        Returns
        -------
        None
        """
        self.client = Client()
        self.task1 = Task.objects.create(
            title='API Task 1',
            description='First API task',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
            priority='LOW',
            status='TODO',
        )
        self.task2 = Task.objects.create(
            title='API Task 2',
            description='Second API task',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=2),
            priority='HIGH',
            status='DOING',
        )
    
    def test_get_new_task_template(self):
        """
        Test retrieving the new_task template via the API.

        Returns
        -------
        None
        """
        url = reverse('tasks:new_task')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form_create', response.content.decode())

    def test_get_all_tasks(self):
        """
        Test retrieving all tasks via the API.

        Returns
        -------
        None
        """
        url = reverse('tasks:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('API Task 1', response.content.decode())
        self.assertIn('API Task 2', response.content.decode())

    def test_search_tasks_valid(self):
        """
        Test searching for tasks with valid parameters via the API.

        Returns
        -------
        None
        """
        url = reverse('tasks:index')
        response = self.client.get(url, {'search': 'API Task 1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('API Task 1', response.content.decode())

    def test_search_tasks_invalid(self):
        """
        Test searching for tasks with invalid parameters returns 400.

        Returns
        -------
        None
        """
        url = reverse('tasks:index')
        response = self.client.get(url, {'search': '!@API Task 1 Invalid@!'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid search parameters', response.content.decode())

    def test_get_task_by_id_success(self):
        """
        Test retrieving a task by ID via the API.

        Returns
        -------
        None
        """
        url = reverse('tasks:task-detail', args=[self.task1.task_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('API Task 1', response.content.decode())

    def test_get_task_by_id_not_found(self):
        """
        Test retrieving a non-existent task by ID returns 404.

        Returns
        -------
        None
        """
        url = reverse('tasks:task-detail', args=[uuid4()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Task not found', response.content.decode())

    def test_create_task_success(self):
        """
        Test creating a new task via the API.

        Returns
        -------
        None
        """
        url = reverse('tasks:create')
        data = {
            'title': 'API Task 3',
            'description': 'Third API task',
            'start_time': datetime.now(timezone.utc).isoformat(),
            'end_time': (datetime.now(timezone.utc) + timedelta(hours=3)).isoformat(),
            'priority': 'MEDIUM',
            'status': 'TODO',
        }
        data = json.dumps(data)
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='API Task 3').exists())

    def test_create_task_failure(self):
        """
        Test creating a new task with missing required fields returns 500.

        Returns
        -------
        None
        """
        url = reverse('tasks:create')
        data = {'title': 'Incomplete Task'}
        data = json.dumps(data)
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Internal Server Error', response.content.decode())

    def test_update_task_success(self):
        """
        Test updating an existing task via the API.

        Returns
        -------
        None
        """
        url = reverse('tasks:task-detail', args=[self.task1.task_id])
        data = {
            'task_id': str(self.task1.task_id),
            'title': 'API Task 1 Updated',
            'description': self.task1.description,
            'start_time': self.task1.start_time.isoformat(),
            'end_time': self.task1.end_time.isoformat(),
            'priority': 'HIGH',
            'status': 'DONE',
        }
        data = json.dumps(data)
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'API Task 1 Updated')
        self.assertEqual(self.task1.priority, 'HIGH')
        self.assertEqual(self.task1.status, 'DONE')

    def test_update_task_not_found(self):
        """
        Test updating a non-existent task returns 404.

        Returns
        -------
        None
        """
        url = reverse('tasks:task-detail', args=[uuid4()])
        data = {
            'task_id': str(uuid4()),
            'title': 'Non-existent Task',
            'description': 'Should not exist',
            'start_time': datetime.now(timezone.utc).isoformat(),
            'end_time': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
            'priority': 'LOW',
            'status': 'TODO',
        }
        data = json.dumps(data)
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Task not found', response.content.decode())

    def test_update_task_failure(self):
        """
        Test updating a task with invalid data returns 500.

        Returns
        -------
        None
        """
        url = reverse('tasks:task-detail', args=[self.task1.task_id])
        data = {'task_id': str(self.task1.task_id)}  # Missing required fields
        data = json.dumps(data)
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Internal Server Error', response.content.decode())

    def test_delete_task_success(self):
        """
        Test deleting a task via the API.

        Returns
        -------
        None
        """
        url = reverse('tasks:task-detail', args=[self.task2.task_id])
        data = {'task_id': str(self.task2.task_id)}
        data = json.dumps(data)
        response = self.client.delete(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(task_id=self.task2.task_id).exists())

    def test_delete_task_not_found(self):
        """
        Test deleting a non-existent task returns 404.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        url = reverse('tasks:task-detail', args=[id])
        data = {'task_id': id}
        data = json.dumps(data)
        response = self.client.delete(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Task not found', response.content.decode())

    def test_delete_task_not_found(self):
        """
        Test deleting a task with invalid data returns 500.

        Returns
        -------
        None
        """
        url = reverse('tasks:task-detail', args=[self.task1.task_id])
        data = {'task_id': str(self.task1.task_id)}
        data = json.dumps(data)
        # Simulate error by deleting the task first
        self.task1.delete()
        response = self.client.delete(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Task not found', response.content.decode())
