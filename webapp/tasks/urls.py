from django.urls import path, re_path
from .views import GetAllTasksView, NewTaskView, SearchTaskView, TaskView

###   Manual DI   #########################################
from .services import TaskService
###########################################################


app_name = "tasks"
urlpatterns = [
    path("new_task/", NewTaskView.as_view(), name="new_task"),
    path("", GetAllTasksView.as_view(), kwargs={"service": TaskService()}, name="index"),
    path("", SearchTaskView.as_view(), kwargs={"service": TaskService()}, name="search"),
    path("", TaskView.as_view(), kwargs={"service": TaskService()}, name="create"),
    path("<uuid:task_id>", TaskView.as_view(), kwargs={"service": TaskService()}, name="retrieve"),
    path("<uuid:task_id>", TaskView.as_view(), kwargs={"service": TaskService()}, name="update"),
    path("<uuid:task_id>", TaskView.as_view(), kwargs={"service": TaskService()}, name="delete")
]