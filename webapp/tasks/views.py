import re, json
from datetime import datetime
from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError
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
    IViewGetAll,
    IViewGetByParams,
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
        if task.get('start_time'):
            task["start_time"] = self.isotodatetime(task['start_time'])
        if task.get('end_time'):
            task["end_time"] = self.isotodatetime(task['end_time'])
        return task

    def get(self, request: HttpRequest, id: str, service: IServiceGetById) -> HttpResponse:
        """
        Retrieve and display a specific task by its ID.
        """
        try:
            task = service.get_by_id(TASK_MODEL, id)
            template = loader.get_template("tasks/retrieve.html")
            context = {
                "title": self.title,
                "task": task
            }
            return HttpResponse(template.render(context, request))
        except NotFound as err404:
            print(err404)
            return HttpResponse("Task not found", status=404)
        except Exception as err:
            print(err)
            return HttpResponseServerError("Internal Server Error")

    def post(self, request: HttpRequest, service: IServiceCreate) -> HttpResponseRedirect:
        """
        Create a new task.
        """
        try:
            task = self.json_decode(request.body)
            if service.create(TASK_MODEL, task):
                return HttpResponseRedirect(reverse("tasks:index",))
        except Exception as err:
            print(err)
            return HttpResponseServerError("Internal Server Error")

    def put(self, request: HttpRequest, service: IServiceUpdate) -> HttpResponseRedirect:
        """
        Update an existing task.
        """
        task = self.json_decode(request.body)
        try:
            if service.update(TASK_MODEL, task):
                return HttpResponseRedirect(reverse("tasks:retrieve", args=[task["task_id"]]))
        except NotFound as err404:
            print(err404)
            return HttpResponse("Task not found", status=404)
        except Exception as err:
            print(err)
            return HttpResponseServerError("Internal Server Error")

    def delete(self, request: HttpRequest, service: IServiceDelete) -> HttpResponseRedirect:
        """
        Delete a task.
        """
        task = self.json_decode(request.body)
        try:
            if service.delete(TASK_MODEL, task["task_id"]):
                return HttpResponseRedirect(reverse("tasks:index",))
        except NotFound as err404:
            print(err404)
            return HttpResponse("Task not found", status=404)
        except Exception as err:
            print(err)
            return HttpResponseServerError("Internal Server Error")


class GetAllTasksView(View, IViewGetAll):
    """
    View for retrieving all tasks.

    Inherits from:
        - View
    Implements:
        - IViewGetAll
    """
    title: str = "Tasks"

    def get(self, request: HttpRequest, service: IServiceGetAll) -> HttpResponse:
        """
        Retrieve all tasks.
        """
        try:
            tasks = service.get_all(TASK_MODEL)
            template = loader.get_template("tasks/index.html")
            context = {
                "title": self.title,
                "tasks": tasks
            }
            return HttpResponse(template.render(context, request))
        except Exception as err:
            print(err)
            return HttpResponseServerError("Internal Server Error")


class SearchTaskView(View, IViewGetByParams):
    """
    View for retrieving tasks by search parameters.

    Inherits from:
        - View
    Implements:
        - IViewGetByParams
    """
    title: str = "Tasks"

    def get_by_params(self, request: HttpRequest, service: IServiceGetByParams) -> HttpResponse:
        """
        Retrieve tasks by search parameters.
        """
        try:
            params = request.GET.get("search")
            pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_\-.\s]{1,48}[a-zA-Z0-9]$")
            if not pattern.match(params):
                return HttpResponseBadRequest("Invalid search")
            tasks = service.get_by_params(TASK_MODEL, params)
            template = loader.get_template("tasks/index.html")
            context = {
                "title": self.title,
                "tasks": tasks
            }
            return HttpResponse(template.render(context, request))
        except Exception as err:
            print(err)
            return HttpResponseServerError("Internal Server Error")


class NewTaskView(View):
    """
    View for rendering a new task page.

    Inherits from:
        - View
    """
    title: str = "Tasks"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Render a new task page.
        """
        try:
            template = loader.get_template(f"tasks/new_task.html")
            context = { "title" : self.title}
            return HttpResponse(template.render(context, request))
        except Exception as err:
            print(err)
            return HttpResponseServerError("Internal Server Error")
