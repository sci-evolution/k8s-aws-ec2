import re, json
from datetime import datetime
from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError
from django.template import loader
from django.urls import reverse
from django.views import View
from .models import Task
from .exceptions import NotFound
from .interfaces import (
    IServiceGetAll,
    IServiceGetByParams,
    IServiceGetById,
    IServiceCreate,
    IServiceUpdate,
    IServiceDelete,
    IViewGetList,
    IViewGetById,
    IViewCreate,
    IViewUpdate,
    IViewDelete
)


TASK_MODEL = Task()  # Provisory model instance for type hinting and dependency injection

class TaskView(
    View,
    IViewGetById,
    IViewCreate,
    IViewUpdate,
    IViewDelete
):
    """
    View layer for Task operations. Handles HTTP requests and responses for tasks.

    Inherits from:
        - View
    Implements:
        - IViewGetById
        - IViewCreate
        - IViewUpdate
        - IViewDelete
    """
    title: str = "Tasks"

    def __repr__(self) -> str:
        """
        Return a string representation of the TaskView instance.
        """
        return "<TaskView>"

    def isotodatetime(self, iso: str) -> datetime:
        """
        Converts a UTC ISO 8601 formatted string (e.g., "YYYY-MM-DDTHH:mm:ss.sssZ")
        to a timezone-aware UTC datetime object.
        """
        dt: datetime = datetime.fromisoformat(iso)
        return dt

    def json_decode(self, json_src: str) -> Dict[str, Any]:
        """
        Convert a JSON string into a dictionary, parsing datetime fields if present.
        """
        task: Dict[str, Any] = json.loads(json_src)
        if task.get("start_time"):
            task["start_time"] = self.isotodatetime(task["start_time"])
        if task.get("end_time"):
            task["end_time"] = self.isotodatetime(task["end_time"])
        return task

    def post(self, request: HttpRequest, service: IServiceCreate) -> HttpResponse:
        """
        Create a new task and return as JSON.
        """
        try:
            data = self.json_decode(request.body)
            task = service.create(TASK_MODEL, data)
            if task:
                return JsonResponse({"success": True, "data": task}, status=201)
            return JsonResponse({"success": False, "error": "Task not created"}, status=400)
        except Exception as err:
            print(err)
            return JsonResponse({"success": False, "error": "Internal Server Error"}, status=500)

    def get(self, request: HttpRequest, id: str, service: IServiceGetById) -> HttpResponse:
        """
        Retrieve a specific task by its ID and return as JSON.
        """
        try:
            _ = request  # Unused parameter, but kept for interface compliance
            task = service.get_by_id(TASK_MODEL, id)
            return JsonResponse({"success": True, "data": task}, status=200)
        except NotFound as err404:
            print(err404)
            return JsonResponse({"success": False, "error": "Task not found"}, status=404)
        except Exception as err:
            print(err)
            return JsonResponse({"success": False, "error": "Internal Server Error"}, status=500)

    def put(self, request: HttpRequest, id: str, service: IServiceUpdate) -> HttpResponse:
        """
        Update an existing task and return as JSON.
        """
        try:
            _ = id  # Unused parameter, but kept for interface compliance
            data = self.json_decode(request.body)
            task = service.update(TASK_MODEL, data)
            if task:
                return JsonResponse({"success": True, "data": task}, status=200)
            return JsonResponse({"success": False, "error": "Task not updated"}, status=400)
        except NotFound as err404:
            print(err404)
            return JsonResponse({"success": False, "error": "Task not found"}, status=404)
        except Exception as err:
            print(err)
            return JsonResponse({"success": False, "error": "Internal Server Error"}, status=500)

    def delete(self, request: HttpRequest, id: str, service: IServiceDelete) -> HttpResponse:
        """
        Delete a task and return as JSON.
        """
        try:
            _ = request  # Unused parameter, but kept for interface compliance
            if service.delete(TASK_MODEL, id):
                return JsonResponse({"success": True, "message": "Task deleted"}, status=204)
            return JsonResponse({"success": False, "error": "Task not deleted"}, status=400)
        except NotFound as err404:
            print(err404)
            return JsonResponse({"success": False, "error": "Task not found"}, status=404)
        except Exception as err:
            print(err)
            return JsonResponse({"success": False, "error": "Internal Server Error"}, status=500)


class GetTasksView(View, IViewGetList):
    """
    View for retrieving a list of tasks.

    Inherits from:
        - View
    Implements:
        - IViewGetList
    """
    title: str = "Tasks"

    def __repr__(self) -> str:
        """
        Return a string representation of the GetTasksView instance.
        """
        return "<GetTasksView>"

    def get(self, request: HttpRequest, service: IServiceGetByParams | IServiceGetAll) -> HttpResponse:
        """
        Retrieve tasks either by search parameters or all tasks, return as JSON.
        """
        try:
            params = request.GET.get("search")
            if params:
                pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_\-.\s]{1,48}[a-zA-Z0-9]$")
                if pattern.match(params) is None:
                    print(f"Invalid search parameters")
                    return JsonResponse({"success": False, "error": "Invalid search parameters"}, status=400)
                tasks = service.get_by_params(TASK_MODEL, params)
            else:
                tasks = service.get_all(TASK_MODEL)
            return JsonResponse({"success": True, "data": tasks}, status=200)
        except Exception as err:
            print(err)
            return JsonResponse({"success": False, "error": "Internal Server Error"}, status=500)
