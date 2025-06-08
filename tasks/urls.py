from django.urls import path
from . import views

###   Manual DI   #########################################
from .services import TaskService
###########################################################


app_name = "users"
urlpatterns = [
    path("", views.get_all, name="index"),
    path("search/", views.get_by_params, name="search"),
    path("new_task/", views.new_task, name="new_task"),
    path("create/", views.create, name="create"),
    path("<uuid:task_id>/", views.TaskView().get_by_id, kwargs={"service": TaskService()}, name="retrieve"),
    path("<uuid:task_id>/update/", views.update, name="update"),
    path("<uuid:task_id>/delete/", views.delete, name="delete")
]