from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "priority", "status"]
    list_filter = ["title", "priority", "status"]
    search_fields = ["title", "priority", "status"]
    fieldsets = [
        (None, {
            "fields": ["title", "priority", "status"]
        }),
        ("Date information", {
            "fields": ["start_time", "end_time"]
        }),
        ("Other informations", {
            "fields": ["description"],
            "classes": ["collapse"]
        })
    ]

admin.site.register(Task, TaskAdmin)
