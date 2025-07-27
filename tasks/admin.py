from django.contrib import admin

from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "created_at"]
    list_filter = ["user", "created_at"]
    search_fields = ["name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "project",
        "status",
        "priority",
        "deadline",
        "created_at",
    ]
    list_filter = ["status", "priority", "project__user", "created_at"]
    search_fields = ["name", "project__name"]
    list_editable = ["status", "priority"]
