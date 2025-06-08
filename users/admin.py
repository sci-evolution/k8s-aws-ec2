from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "joined_at", "is_active"]
    list_filter = ["name", "joined_at", "is_active"]
    search_fields = ["name", "joined_at", "is_active"]
    fieldsets = [
        (None, {
            "fields": ["name", "joined_at", "is_active"]
        }),
        ("Personal Information", {
            "fields": ["age", "gender"]
        }),
        ("Other Informations", {
            "fields": ["obs"],
            "classes": ["colapse"]
        })
    ]

admin.site.register(User, UserAdmin)