import re, json
from datetime import datetime
from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
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

class TaskView():
    title: str = "Tasks"

    def isotodatetime(self, iso: str) -> datetime:
        """
        Converts an ISO 8601 formatted string to a datetime object.
        """
        dt: datetime = datetime.fromisoformat(iso + "Z")
        return dt
    
    def json_decode(self, json_src: str) -> Dict[str, Any]:
        """
        To convert a json into a dict
        """
        task: Dict[str, Any] = json.loads(json_src)
        task["start_time"] = self.isotodatetime(task['start_time']) if task['start_time'] else None
        task["end_time"] = self.isotodatetime(task['end_time']) if task['end_time'] else None
        return task

    def new_task(self, request: HttpRequest):
        try:
            template = loader.get_template("tasks/create.html")
            context = { "title" : self.title}
            return HttpResponse(template.render(context, request))
        except Exception as err:
            print(err)
            raise
    
    def get_all(self, request: HttpRequest) -> HttpResponse:
        try:
            tasks = TaskService().get_all()
            template = loader.get_template("tasks/index.html")
            context = {
                "title": title,
                "tasks": tasks
            }
            return HttpResponse(template.render(context, request))
        except Exception as err:
            print(err)
            raise
    
    def get_by_params(self, request: HttpRequest):
        try:
            params = request.GET.get("search")
            pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_\-.\s]{1,48}[a-zA-Z0-9]$")
            
            if(not pattern.match(params)):
                return HttpResponseBadRequest("Invalid search")
            
            tasks = TaskService().get_by_params(params)
            template = loader.get_template("tasks/index.html")
            context = {
                "title": title,
                "tasks": tasks
            }
            return HttpResponse(template.render(context, request))
        except Exception as err:
            print(err)
            raise

    def get_by_id(self, request: HttpRequest, id: str, service: IServiceGetById) -> HttpResponse:
        try:
            task = service.get_by_id(id, Task())
            template = loader.get_template("tasks/retrieve.html")
            context = {
                "title": title,
                "task": task
            }
            return HttpResponse(template.render(context, request))
        except NotFound as err404:
            print(err404)
            raise Http404("User not found!") from err404
        except Exception as err:
            print(err)
            raise
    
    def create(self, request: HttpRequest):
        try:
            task = json_decode(request.body)
            if(TaskService().create(task)):
                return HttpResponseRedirect(reverse("tasks:index",))
        except Exception as err:
            print(err)
            raise
    
    def update(self, request: HttpRequest, task_id: str):
        task = json_decode(request.body)
        task["task_id"] = task_id
        
        try:
            if(TaskService().update(task)):
                return HttpResponseRedirect(reverse("tasks:retrieve", args=[task["task_id"]]))
        except NotFound as err404:
            print(err404)
            raise Http404("Task not found!") from err404
        except Exception as err:
            print(err)
            raise
    
    def delete(self, request: HttpRequest, task_id: str):
        try:
            if(TaskService().delete(task_id)):
                return HttpResponseRedirect(reverse("tasks:index",))
        except NotFound as err404:
            print(err404)
            raise Http404("Task not found!") from err404
        except Exception as err:
            print(err)
            raise
