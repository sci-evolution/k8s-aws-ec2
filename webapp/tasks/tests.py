from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from django.test import TestCase
from .models import Task

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
