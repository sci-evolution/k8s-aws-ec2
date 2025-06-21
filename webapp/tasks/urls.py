from django.urls import path, re_path
from .views import TaskView, GetTasksView, NewTaskView

###   Manual DI   #########################################
from .services import TaskService
###########################################################


app_name = "tasks"
urlpatterns = [
    path("", GetTasksView.as_view(), kwargs={"service": TaskService()}, name="index"),
    path("create", TaskView.as_view(), kwargs={"service": TaskService()}, name="create"),
    path("<uuid:id>", TaskView.as_view(), kwargs={"service": TaskService()}, name="task-detail"),
    path("new_task", NewTaskView.as_view(), name="new_task")
]