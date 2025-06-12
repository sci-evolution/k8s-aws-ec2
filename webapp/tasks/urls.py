from django.urls import path
from . import views

###   Manual DI   #########################################
from .services import TaskService
###########################################################


app_name = "users"
urlpatterns = [
    path("", views.TaskView.get_all, name="index"),
    path("search/", views.TaskView.get_by_params, kwargs={"service": TaskService()}, name="search"),
    path("new_task/", views.TaskView.new_task, kwargs={"service": TaskService()}, name="new_task"),
    path("create/", views.TaskView.create, kwargs={"service": TaskService()}, name="create"),
    path("<uuid:task_id>/", views.TaskView.get_by_id, kwargs={"service": TaskService()}, name="retrieve"),
    path("<uuid:task_id>/update/", views.TaskView.update, kwargs={"service": TaskService()}, name="update"),
    path("<uuid:task_id>/delete/", views.TaskView.delete, kwargs={"service": TaskService()}, name="delete")
]