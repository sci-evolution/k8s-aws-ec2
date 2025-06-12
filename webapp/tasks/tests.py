from uuid import uuid4
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from django.test import TestCase
from unittest.mock import Mock
from django.http import Http404, HttpRequest

from .exceptions import NotFound
from .models import Task
from .views import TaskView
from .interfaces import IServiceGetAll, IServiceGetByParams, IServiceGetById, IServiceCreate, IServiceUpdate, IServiceDelete


class TaskModelTests(TestCase):
    def setUp(self):
        self.task = Task()
        self.task_data: List[Dict[str, Any]] = []

        for t in range(1, 4):
            data = {
                'task_id': None,  # Will be set by model
                'title': f'Test Task {t}',
                'description': f'A test task {t}',
                'start_time': datetime.now(timezone.utc),
                'end_time': datetime.now(timezone.utc) + timedelta(hours=1),
                'priority': 'HIGH' if t % 2 == 0 else 'LOW',
                'status': 'TODO' if t % 2 == 0 else 'DONE',
            }
            self.task_data.append(data)
            self.task_data[-1]["task_id"] = Task.objects.create(**data).task_id

    def test_custom_get_all(self):
        tasks = self.task.custom_get_all()
        self.assertEqual(len(tasks), 3)

    def test_custom_get_by_params(self):
        params = 'Test Task 2'
        tasks = self.task.custom_get_by_params(params)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], self.task_data[1]['title'])
        self.assertEqual(tasks[0]['priority'], self.task_data[1]['priority'])
        self.assertEqual(tasks[0]['status'], self.task_data[1]['status'])

    def test_custom_get_by_id(self):
        id = str(self.task_data[1]['task_id'])
        task_dict = self.task.custom_get_by_id(id)
        self.assertEqual(task_dict['title'], self.task_data[1]['title'])
        self.assertEqual(task_dict['priority'], self.task_data[1]['priority'])

    def test_custom_create(self):
        new_task_data = {
            'title': 'New Task',
            'description': 'A new task',
            'start_time': datetime.now(timezone.utc),
            'end_time': datetime.now(timezone.utc) + timedelta(hours=1),
            'priority': 'LOW',
            'status': 'TODO',
        }
        created = self.task.custom_create(new_task_data)
        self.assertTrue(created)
        self.assertEqual(Task.objects.count(), 4)

    def test_custom_update(self):
        updated_data = self.task_data[0].copy()
        updated_data['task_id'] = str(self.task_data[1]['task_id'])
        updated_data['title'] = 'Updated Task'
        updated_data['priority'] = 'HIGH'
        updated = self.task.custom_update(updated_data)
        self.assertTrue(updated)
        updated_task = Task.objects.get(pk=self.task_data[1]['task_id'])
        self.assertEqual(updated_task.title, 'Updated Task')
        self.assertEqual(updated_task.priority, 'HIGH')

    def test_custom_delete(self):
        task_id = str(self.task_data[1]['task_id'])
        deleted = self.task.custom_delete(task_id)
        self.assertTrue(deleted)
        self.assertEqual(Task.objects.count(), 2)


class TaskViewTests(TestCase):
    def setUp(self):
        self.view = TaskView()
        self.request = HttpRequest()
        self.request.method = 'GET'

    def test_get_all(self):
        id: str = str(uuid4())
        tasks: List[Dict[str, Any]] = [
            {
                'task_id': id,
                'title': 'Task Y',
                'start_time': None,
                'end_time': None,
                'priority': 'LOW',
                'status': 'TODO'
            }
        ]
        mock_service = Mock(spec=IServiceGetAll)
        mock_service.get_all.return_value = tasks
        response = self.view.get_all(self.request, mock_service)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task Y', response.content.decode())

    def test_get_by_params_valid(self):
        id: str = str(uuid4())
        tasks: List[Dict[str, Any]] = [
            {
                'task_id': id,
                'title': 'Task Y',
                'start_time': None,
                'end_time': None,
                'priority': 'LOW',
                'status': 'TODO'
            }
        ]
        mock_service = Mock(spec=IServiceGetByParams)
        mock_service.get_by_params.return_value = tasks
        self.request.GET['search'] = 'Task Y'
        response = self.view.get_by_params(self.request, mock_service)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task Y', response.content.decode())

    def test_get_by_params_invalid(self):
        mock_service = Mock(spec=IServiceGetByParams)
        self.request.GET['search'] = '!@#invalid!'
        response = self.view.get_by_params(self.request, mock_service)
        self.assertEqual(response.status_code, 400)

    def test_get_by_id(self):
        id: str = str(uuid4())
        task: Dict[str, Any] = {
            'task_id': id,
            'title': 'Task Y',
            'start_time': None,
            'end_time': None,
            'priority': 'LOW',
            'status': 'TODO'
        }
        mock_service = Mock(spec=IServiceGetById)
        mock_service.get_by_id.return_value = task
        response = self.view.get_by_id(self.request, id, mock_service)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task Y', response.content.decode())
    
    def test_get_by_id_not_found(self):
        mock_service = Mock(spec=IServiceGetById)
        mock_service.get_by_id.side_effect = NotFound("Task not found")
        with self.assertRaises(Http404):
            self.view.get_by_id(self.request, 'non-existent-id', mock_service)

    def test_create_success(self):
        mock_service = Mock(spec=IServiceCreate)
        mock_service.create.return_value = True
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = b'{"title": "Task Z", "start_time": null, "end_time": null, "priority": "LOW", "status": "TODO"}'
        response = self.view.create(mock_request, mock_service)
        self.assertEqual(response.status_code, 302)

    def test_update_success(self):
        id: str = str(uuid4())
        body = f"{{\"task_id\": \"{id}\", \"title\": \"Task U\", \"start_time\": null, \"end_time\": null, \"priority\": \"LOW\", \"status\": \"TODO\"}}"
        mock_service = Mock(spec=IServiceUpdate)
        mock_service.update.return_value = True
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = body.encode('utf-8')
        response = self.view.update(mock_request, mock_service)
        self.assertEqual(response.status_code, 302)
    
    def test_update_failure(self):
        id: str = str(uuid4())
        body = f'{{"task_id": "{id}", "title": "Task U", "start_time": null, "end_time": null, "priority": "LOW", "status": "TODO"}}'
        mock_service = Mock(spec=IServiceUpdate)
        mock_service.update.side_effect = NotFound("Task not found")
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = body.encode('utf-8')
        with self.assertRaises(Http404):
            self.view.update(mock_request, mock_service)

    def test_delete_success(self):
        id: str = str(uuid4())
        body = f'{{"task_id": "{id}"}}'
        mock_service = Mock(spec=IServiceDelete)
        mock_service.delete.return_value = True
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = body.encode('utf-8')
        response = self.view.delete(mock_request, mock_service)
        self.assertEqual(response.status_code, 302)
    
    def test_delete_failure(self):
        id: str = str(uuid4())
        body = f'{{"task_id": "{id}"}}'
        mock_service = Mock(spec=IServiceDelete)
        mock_service.delete.side_effect = NotFound("Task not found")
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = body.encode('utf-8')
        with self.assertRaises(Http404):
            self.view.delete(mock_request, mock_service)
