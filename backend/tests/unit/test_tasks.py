import json
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from unittest.mock import Mock
from django.test import TestCase
from django.http import HttpRequest
from tasks.interfaces import IServiceGetAll, IServiceGetByParams, IServiceGetById, IServiceCreate, IServiceUpdate, IServiceDelete
from tasks.exceptions import NotFound
from tasks.models import Task
from tasks.services import TaskService
from tasks.views import GetTasksView, TaskView


class TaskModelTests(TestCase):
    """
    Unit tests for the Task model and its custom methods.
    """
    def setUp(self):
        """
        Set up test data for Task model tests.

        Returns
        -------
        None
        """
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

    def test_task_str_success(self):
        """
        Test the string representation of the Task model.

        Returns
        -------
        None
        """
        task = Task.objects.first()
        self.assertEqual(str(task), f"Task(id={task.task_id}, title={task.title})")

    def test_task_repr_success(self):
        """
        Test the string representation of the Task model.

        Returns
        -------
        None
        """
        task = Task.objects.first()
        self.assertIsInstance(repr(task), str)
        self.assertIn("task_id", repr(task))
        self.assertIn("title", repr(task))
        self.assertIn("description", repr(task))
        self.assertIn("start_time", repr(task))
        self.assertIn("end_time", repr(task))
        self.assertIn("PRIORITY_CHOICES", repr(task))
        self.assertIn("priority", repr(task))
        self.assertIn("STATUS_CHOICES", repr(task))
        self.assertIn("status", repr(task))

    def test_datetimetoiso_returns_iso8601_string(self):
        """
        Test that datetimetoiso returns a valid ISO 8601 string.

        Returns
        -------
        None
        """
        dt = datetime(2025, 6, 17, 12, 34, 56, tzinfo=timezone.utc)
        iso = self.task.datetimetoiso(dt)
        self.assertTrue(iso.startswith("2025-06-17T12:34"))
        self.assertIn("T", iso)

    def test_custom_get_all_returns_all_tasks(self):
        """
        Test retrieving all tasks.

        Returns
        -------
        None
        """
        tasks = self.task.custom_get_all()
        self.assertEqual(len(tasks), 3)

    def test_custom_get_by_params_filters_tasks(self):
        """
        Test retrieving tasks by parameters.

        Returns
        -------
        None
        """
        params = 'Test Task 2'
        tasks = self.task.custom_get_by_params(params)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], self.task_data[1]['title'])
        self.assertEqual(tasks[0]['priority'], self.task_data[1]['priority'])
        self.assertEqual(tasks[0]['status'], self.task_data[1]['status'])

    def test_custom_get_by_id_returns_task(self):
        """
        Test retrieving a task by its ID.

        Returns
        -------
        None
        """
        id = str(self.task_data[1]['task_id'])
        task_dict = self.task.custom_get_by_id(id)
        self.assertEqual(task_dict['title'], self.task_data[1]['title'])
        self.assertEqual(task_dict['priority'], self.task_data[1]['priority'])

    def test_custom_get_by_id_raises_notfound(self):
        """
        Test that custom_get_by_id raises NotFound when the task does not exist.

        Returns
        -------
        None
        """
        invalid_id = str(uuid4())
        with self.assertRaises(NotFound):
            self.task.custom_get_by_id(invalid_id)

    def test_custom_create_success_returns_created_task(self):
        """
        Test creating a new task.

        Returns
        -------
        None
        """
        new_task_data = {
            "title": "New Task",
            "description": "A new task",
            "start_time": datetime.now(timezone.utc),
            "end_time": datetime.now(timezone.utc) + timedelta(hours=1),
            "priority": "LOW",
            "status": "TODO",
        }
        created = self.task.custom_create(new_task_data)
        self.assertIsInstance(created, Dict)
        self.assertEqual(created["title"], new_task_data["title"])

    def test_custom_create_fail_raises_exception(self):
        """
        Test that custom_create raises Exception on error (simulate by omitting required fields).

        Returns
        -------
        None
        """
        bad_data = {'title': 'Bad Task'}  # Missing required fields
        with self.assertRaises(Exception):
            self.task.custom_create(bad_data)

    def test_custom_update_success_returns_updated_task(self):
        """
        Test updating an existing task.

        Returns
        -------
        None
        """
        data = self.task_data[0].copy()
        data['title'] = 'Updated Task'
        data['priority'] = 'HIGH'
        updated = self.task.custom_update(data)
        self.assertIsInstance(updated, Dict)
        self.assertEqual(updated['task_id'], data['task_id'])
        self.assertEqual(updated['title'], 'Updated Task')
        self.assertEqual(updated['priority'], 'HIGH')

    def test_custom_update_fails_raises_notfound(self):
        """
        Test that custom_update raises NotFound when the task does not exist.

        Returns
        -------
        None
        """
        invalid_data = self.task_data[0].copy()
        invalid_data['task_id'] = str(uuid4())
        with self.assertRaises(NotFound):
            self.task.custom_update(invalid_data)

    def test_custom_delete_deletes_task(self):
        """
        Test deleting a task by its ID.

        Returns
        -------
        None
        """
        task_id = str(self.task_data[1]['task_id'])
        deleted = self.task.custom_delete(task_id)
        self.assertTrue(deleted)
        self.assertEqual(Task.objects.count(), 2)

    def test_custom_delete_raises_notfound(self):
        """
        Test that custom_delete raises NotFound when the task does not exist.

        Returns
        -------
        None
        """
        invalid_id = str(uuid4())
        with self.assertRaises(NotFound):
            self.task.custom_delete(invalid_id)


class TaskServiceTests(TestCase):
    """
    Unit tests for the TaskService business logic layer.
    """
    def setUp(self):
        """
        Set up mock model and service for TaskService tests.

        Returns
        -------
        None
        """
        self.model = Mock()
        self.service = TaskService()
        self.data: List[Dict[str, Any]] = [
            {
                'task_id': str(uuid4()),
                'title': 'Service Task',
                'start_time': datetime.now(timezone.utc),
                'end_time': datetime.now(timezone.utc) + timedelta(hours=1),
                'priority': 'LOW',
                'status': 'TODO'
            }
        ]

    def test_service_repr_success(self):
        """
        Test the string representation of the TaskService.

        Returns
        -------
        None
        """
        self.assertEqual(repr(self.service), "<TaskService>")

    def test_service_get_all_returns_all_tasks(self):
        """
        Test retrieving all tasks via the service.

        Returns
        -------
        None
        """
        self.model.custom_get_all.return_value = self.data
        result = self.service.get_all(self.model)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['title'], self.data[0]['title'])

    def test_service_get_by_params_filters_tasks(self):
        """
        Test retrieving tasks by params via the service.

        Returns
        -------
        None
        """
        self.model.custom_get_by_params.return_value = self.data
        result = self.service.get_by_params(self.model, 'Service')
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['title'], self.data[0]['title'])

    def test_service_get_by_id_returns_task(self):
        """
        Test retrieving a task by ID via the service.

        Returns
        -------
        None
        """
        self.model.custom_get_by_id.return_value = self.data[0]
        result = self.service.get_by_id(self.model, self.data[0]['task_id'])
        self.assertIsInstance(result, dict)
        self.assertEqual(result['title'], self.data[0]['title'])

    def test_service_create_success_returns_created_task(self):
        """
        Test creating a task via the service.

        Returns
        -------
        None
        """
        data: Dict[str, Any] = {
            'title': 'Service Task',
            'start_time': datetime.now(timezone.utc),
            'end_time': datetime.now(timezone.utc) + timedelta(hours=1),
            'priority': 'LOW',
            'status': 'TODO'
        }
        self.model.custom_create.return_value = data
        created = self.service.create(self.model, data)
        self.assertIsInstance(created, Dict)
        self.assertEqual(created['title'], data['title'])

    def test_service_update_updates_task(self):
        """
        Test updating a task via the service.

        Returns
        -------
        None
        """
        data: Dict[str, Any] = {
            'task_id': str(uuid4()),
            'title': 'Service Task Updated',
            'start_time': datetime.now(timezone.utc),
            'end_time': None,
            'priority': 'LOW',
            'status': 'DONE' # Set to DONE to trigger end_time update
        }
        self.model.custom_update.return_value = data
        updated = self.service.update(self.model, data)
        self.assertIsInstance(updated, Dict)
        self.assertEqual(updated['title'], data['title'])

    def test_service_delete_deletes_task(self):
        """
        Test deleting a task via the service.

        Returns
        -------
        None
        """
        self.model.custom_delete.return_value = True
        id: str = str(uuid4())
        deleted = self.service.delete(self.model, id)
        self.assertTrue(deleted)
        self.model.custom_delete.assert_called_once_with(id)


class TaskViewTests(TestCase):
    """
    Unit tests for the TaskView HTTP layer.
    """
    def setUp(self):
        """
        Set up a TaskView instance and a mock request for view tests.

        Returns
        -------
        None
        """
        self.view = TaskView()
    
    def test_view_representation_success(self):
        """
        Test the string representation of the TaskView.

        Returns
        -------
        None
        """
        self.assertEqual(repr(self.view), "<TaskView>")

    def test_view_isotodatetime_success_parses_iso_string(self):
        """
        Test converting ISO 8601 string to datetime.

        Returns
        -------
        None
        """
        iso = "2025-06-17T18:30:00.000Z"
        dt = self.view.isotodatetime(iso)
        self.assertIsInstance(dt, datetime)
        self.assertEqual(dt.year, 2025)
        self.assertEqual(dt.month, 6)
        self.assertEqual(dt.day, 17)
        self.assertEqual(dt.hour, 18)
        self.assertEqual(dt.minute, 30)
        self.assertEqual(dt.second, 0)

    def test_view_json_decode_success_parses_json(self):
        """
        Test decoding a JSON string to a dictionary with datetime fields.

        Returns
        -------
        None
        """
        body: Dict[str, Any] = {
            "title": "Task Z",
            "start_time": "2025-06-17T18:30:00.000Z",
            "end_time": "2025-06-18T18:30:00.000Z",
            "priority": "LOW",
            "status": "TODO"
        }
        json_str = json.dumps(body)
        result = self.view.json_decode(json_str)
        self.assertEqual(result['title'], 'Task Z')
        self.assertIsInstance(result['start_time'], datetime)
        self.assertIsInstance(result['end_time'], datetime)
        self.assertEqual(result['priority'], 'LOW')
        self.assertEqual(result['status'], 'TODO')

    def test_view_get_by_id_success_returns_task(self):
        """
        Test retrieving a task by ID via the view.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        task: Dict[str, Any] = {
            'task_id': id,
            'title': 'Task Y',
            'start_time': None,
            'end_time': None,
            'priority': 'LOW',
            'status': 'TODO'
        }
        request: HttpRequest = HttpRequest()
        request.method = 'GET'
        mock_service = Mock(spec=IServiceGetById)
        mock_service.get_by_id.return_value = task
        response = self.view.get(request, id, mock_service)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task Y', response.content.decode())

    def test_view_get_by_id_failure_returns_error_404(self):
        """
        Test handling NotFound exception when retrieving by ID via the view.

        Returns
        -------
        None
        """
        request: HttpRequest = HttpRequest()
        request.method = 'GET'
        mock_service = Mock(spec=IServiceGetById)
        mock_service.get_by_id.side_effect = NotFound("Task not found")
        response = self.view.get(request, 'non-existent-id', mock_service)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Task not found", response.content.decode())

    def test_view_get_by_id_failure_returns_error_500(self):
        """
        Test handling any exceptions when retrieving by ID via the view.

        Returns
        -------
        None
        """
        request: HttpRequest = HttpRequest()
        request.method = 'GET'
        mock_service = Mock(spec=IServiceGetById)
        mock_service.get_by_id.side_effect = Exception("Unexpected error")
        response = self.view.get(request, 'non-existent-id', mock_service)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal Server Error", response.content.decode())

    def test_view_create_success_returns_created_task(self):
        """
        Test successful creation of a task via the view.

        Returns
        -------
        None
        """
        body: Dict[str, Any] = {
            "title": "Task Z",
            "start_time": None,
            "end_time": None,
            "priority": "LOW",
            "status": "TODO"
        }
        json_str = json.dumps(body)
        mock_service = Mock(spec=IServiceCreate)
        mock_service.create.return_value = body
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = json_str
        response = self.view.post(mock_request, mock_service)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Task Z", response.content.decode())

    def test_view_create_failure_returns_error_500(self):
        """
        Test handling any exceptions when creating a task via the view.

        Returns
        -------
        None
        """
        body: Dict[str, Any] = {
            "title": "Task Z",
            "start_time": None,
            "end_time": None,
            "priority": "LOW",
            "status": "TODO"
        }
        json_str = json.dumps(body)
        mock_service = Mock(spec=IServiceCreate)
        mock_service.create.side_effect = Exception("Unexpected error")
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = json_str
        response = self.view.post(mock_request, mock_service)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal Server Error", response.content.decode())

    def test_view_update_success_returns_updated_task(self):
        """
        Test successful update of a task via the view.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        body: Dict[str, Any] = {
            "task_id": id,
            "title": "Task U",
            "start_time": None,
            "end_time": None,
            "priority": "LOW",
            "status": "TODO"
        }
        json_str = json.dumps(body)
        mock_service = Mock(spec=IServiceUpdate)
        mock_service.update.return_value = body
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = json_str
        response = self.view.put(mock_request, id, mock_service)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task U', response.content.decode())

    def test_view_update_failure_returns_error_404(self):
        """
        Test handling NotFound exception when updating via the view.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        body: Dict[str, Any] = {
            "task_id": id,
            "title": "Task Z",
            "start_time": None,
            "end_time": None,
            "priority": "LOW",
            "status": "TODO"
        }
        json_str = json.dumps(body)
        mock_service = Mock(spec=IServiceUpdate)
        mock_service.update.side_effect = NotFound("Task not found")
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = json_str
        response = self.view.put(mock_request, id, mock_service)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Task not found", response.content.decode())

    def test_view_update_failure_returns_error_500(self):
        """
        Test handling any exceptions when updating a task via the view.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        body: Dict[str, Any] = {
            "task_id": id,
            "title": "Task U",
            "start_time": None,
            "end_time": None,
            "priority": "LOW",
            "status": "TODO"
        }
        json_str = json.dumps(body)
        mock_service = Mock(spec=IServiceUpdate)
        mock_service.update.side_effect = Exception("Unexpected error")
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = json_str
        response = self.view.put(mock_request, id, mock_service)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal Server Error", response.content.decode())

    def test_view_delete_success_returns_success(self):
        """
        Test successful deletion of a task via the view.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        body: Dict[str, Any] = {
            "task_id": id
        }
        json_str = json.dumps(body)
        mock_service = Mock(spec=IServiceDelete)
        mock_service.delete.return_value = True
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = json_str
        response = self.view.delete(mock_request, id, mock_service)
        self.assertEqual(response.status_code, 204)
        self.assertIn("Task deleted", response.content.decode())

    def test_view_delete_failure_returns_error_404(self):
        """
        Test handling NotFound exception when deleting via the view.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        body: Dict[str, Any] = {
            "task_id": id
        }
        json_str = json.dumps(body)
        mock_service = Mock(spec=IServiceDelete)
        mock_service.delete.side_effect = NotFound("Task not found")
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = json_str
        response = self.view.delete(mock_request, id, mock_service)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Task not found", response.content.decode())

    def test_view_delete_failure_returns_error_500(self):
        """
        Test handling any exceptions when deleting a task via the view.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        body: Dict[str, Any] = {
            "task_id": id
        }
        json_str = json.dumps(body)
        mock_service = Mock(spec=IServiceDelete)
        mock_service.delete.side_effect = Exception("Unexpected error")
        mock_request = Mock(spec=HttpRequest)
        mock_request.body = json_str
        response = self.view.delete(mock_request, id, mock_service)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal Server Error", response.content.decode())


class GetTasksViewTests(TestCase):
    """
    Unit tests for the GetTasksView.
    """
    def setUp(self):
        """
        Set up a GetTasksView instance and a mock request for view tests.

        Returns
        -------
        None
        """
        self.view = GetTasksView()
    
    def test_view_representation_success(self):
        """
        Test the string representation of the GetTasksView.

        Returns
        -------
        None
        """
        self.assertEqual(repr(self.view), "<GetTasksView>")

    def test_view_get_all_success_returns_tasks(self):
        """
        Test retrieving all tasks.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        tasks: List[Dict[str, Any]] = [
            {
                'task_id': id,
                'title': 'Get All Tasks',
                'start_time': None,
                'end_time': None,
                'priority': 'LOW',
                'status': 'TODO'
            }
        ]
        request: HttpRequest = HttpRequest()
        request.method = 'GET'
        mock_service = Mock(spec=IServiceGetAll)
        mock_service.get_all.return_value = tasks
        response = self.view.get(request, service=mock_service)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Get All Tasks', response.content.decode())

    def test_view_get_all_failure_returns_error_500(self):
        """
        Test handling any exceptions when retrieving all tasks.

        Returns
        -------
        None
        """
        request: HttpRequest = HttpRequest()
        request.method = 'GET'
        mock_service = Mock(spec=IServiceGetAll)
        mock_service.get_all.side_effect = Exception("Unexpected error")
        response = self.view.get(request, service=mock_service)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal Server Error", response.content.decode())

    def test_view_get_search_success_returns_tasks(self):
        """
        Test retrieving tasks by valid search params.

        Returns
        -------
        None
        """
        id: str = str(uuid4())
        tasks: List[Dict[str, Any]] = [
            {
                'task_id': id,
                'title': 'Search Task Valid',
                'start_time': None,
                'end_time': None,
                'priority': 'LOW',
                'status': 'TODO'
            }
        ]
        request: HttpRequest = HttpRequest()
        request.method = 'GET'
        request.GET['search'] = 'Search Task Valid'
        mock_service = Mock(spec=IServiceGetByParams)
        mock_service.get_by_params.return_value = tasks
        response = self.view.get(request, service=mock_service)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Search Task Valid', response.content.decode())

    def test_view_get_search_failure_returns_error_400(self):
        """
        Test retrieving tasks by invalid search params.

        Returns
        -------
        None
        """
        request: HttpRequest = HttpRequest()
        request.method = 'GET'
        mock_service = Mock(spec=IServiceGetByParams)
        request.GET['search'] = '!@Search Task Invalid@!'
        response = self.view.get(request, service=mock_service)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid search parameters", response.content.decode())

    def test_view_get_search_failure_returns_error_500(self):
        """
        Test handling any exceptions when retrieving tasks by search params.

        Returns
        -------
        None
        """
        request: HttpRequest = HttpRequest()
        request.method = 'GET'
        request.GET['search'] = 'Search Task Error 500'
        mock_service = Mock(spec=IServiceGetByParams)
        mock_service.get_by_params.side_effect = Exception("Unexpected error")
        response = self.view.get(request, service=mock_service)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal Server Error", response.content.decode())
