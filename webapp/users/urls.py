from django.urls import path
from . import views


app_name = "users"
# urlpatterns = [
#     path("", views.get_all, name="index"),
#     path("search/", views.get_by_params, name="search"),
#     path("new_user/", views.new_user, name="new_user"),
#     path("create/", views.create, name="create"),
#     path("<uuid:user_id>/", views.UserView().get_by_id, name="task-detail"),
#     path("<uuid:user_id>/update/", views.update, name="update"),
#     path("<uuid:user_id>/delete/", views.delete, name="delete")
# ]