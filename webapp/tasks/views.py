import re, json
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from .models import Task
from .services import TaskService
from .exceptions import NotFound


TITLE: str = "Tasks"

def json_decode(task_json: str) -> dict[str, any]:
    task = json.loads(task_json)
    task["start_time"] = task["start_time"] or None
    task["end_time"] = task["end_time"] or None
    return task

def new_task(request: HttpRequest):
    try:
        template = loader.get_template("tasks/create.html")
        context = { "title" : TITLE}
        return HttpResponse(template.render(context, request))
    except Exception as err:
        print(err)
        raise

def get_all(request: HttpRequest):
    try:
        tasks = TaskService().get_all()
        template = loader.get_template("tasks/index.html")
        context = {
            "title": TITLE,
            "tasks": tasks
        }
        return HttpResponse(template.render(context, request))
    except Exception as err:
        print(err)
        raise

def get_by_params(request: HttpRequest):
    try:
        params = request.GET.get("search")
        pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_\-.\s]{1,48}[a-zA-Z0-9]$")
        
        if(not pattern.match(params)):
            return HttpResponseBadRequest("Invalid search")
        
        tasks = TaskService().get_by_params(params)
        template = loader.get_template("tasks/index.html")
        context = {
            "title": TITLE,
            "tasks": tasks
        }
        return HttpResponse(template.render(context, request))
    except Exception as err:
        print(err)
        raise

###############################################################################
from .interfaces import IViewGetById, IServiceGetById

class TaskView(IViewGetById):
    def get_by_id(self, request: HttpRequest, id: str, service: IServiceGetById) -> HttpResponse:
        try:
            task = service.get_by_id(id, Task())
            template = loader.get_template("tasks/retrieve.html")
            context = {
                "title": TITLE,
                "task": task
            }
            return HttpResponse(template.render(context, request))
        except NotFound as err404:
            print(err404)
            raise Http404("User not found!") from err404
        except Exception as err:
            print(err)
            raise

###############################################################################

def create(request: HttpRequest):
    try:
        task = json_decode(request.body)
        if(TaskService().create(task)):
            return HttpResponseRedirect(reverse("tasks:index",))
    except Exception as err:
        print(err)
        raise

def update(request: HttpRequest, task_id: str):
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

def delete(request: HttpRequest, task_id: str):
    try:
        if(TaskService().delete(task_id)):
            return HttpResponseRedirect(reverse("tasks:index",))
    except NotFound as err404:
        print(err404)
        raise Http404("Task not found!") from err404
    except Exception as err:
        print(err)
        raise
