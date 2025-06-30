from django.urls import path
from .views import TaskView, GetTasksView

###   Manual DI   #########################################
from .services import TaskService
###########################################################


app_name = "tasks"
urlpatterns = [
    path("", GetTasksView.as_view(), kwargs={"service": TaskService()}, name="index"),
    path("create", TaskView.as_view(), kwargs={"service": TaskService()}, name="create"),
    path("<uuid:id>", TaskView.as_view(), kwargs={"service": TaskService()}, name="task-detail")
]