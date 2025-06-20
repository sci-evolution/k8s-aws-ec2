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
        if task.get('start_time'):
            task["start_time"] = self.isotodatetime(task['start_time'])
        if task.get('end_time'):
            task["end_time"] = self.isotodatetime(task['end_time'])
        return task

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

    def put(self, request: HttpRequest, id: str, service: IServiceUpdate) -> HttpResponseRedirect:
        """
        Update an existing task.
        """
        task = self.json_decode(request.body)
        try:
            if service.update(TASK_MODEL, task):
                return HttpResponseRedirect(reverse("tasks:task-detail", args=[id]))
        except NotFound as err404:
            print(err404)
            return HttpResponse("Task not found", status=404)
        except Exception as err:
            print(err)
            return HttpResponseServerError("Internal Server Error")

    def delete(self, request: HttpRequest, id: str, service: IServiceDelete) -> HttpResponseRedirect:
        """
        Delete a task.
        """
        task = self.json_decode(request.body)
        try:
            if service.delete(TASK_MODEL, id):
                return HttpResponseRedirect(reverse("tasks:index",))
        except NotFound as err404:
            print(err404)
            return HttpResponse("Task not found", status=404)
        except Exception as err:
            print(err)
            return HttpResponseServerError("Internal Server Error")


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
        Retrieve tasks either by search parameters or all tasks.
        """
        try:
            tasks = None
            params = request.GET.get("search")
            if params:
                pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_\-.\s]{1,48}[a-zA-Z0-9]$")
                if pattern.match(params) is None:
                    print(f"Invalid search parameters")
                    return HttpResponseBadRequest("Invalid search parameters")
                tasks = service.get_by_params(TASK_MODEL, params)
            else:
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


class NewTaskView(View):
    """
    View for rendering a new task page.

    Inherits from:
        - View
    """
    title: str = "Tasks"

    def __repr__(self) -> str:
        """
        Return a string representation of the NewTaskView instance.
        """
        return "<NewTaskView>"

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
