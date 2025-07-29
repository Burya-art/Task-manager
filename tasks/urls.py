from django.urls import path

from tasks import views

app_name = "tasks"

urlpatterns = [
    # Основні сторінки
    path("project/<int:pk>/", views.ProjectDetailView.as_view(),
        name="project_detail",
    ),

    # HTMX endpoints для проектів
    path(
        "htmx/project/form/",
        views.show_project_form_htmx,
        name="show_project_form_htmx",
    ),
    path(
        "htmx/project/create/",
        views.create_project_htmx,
        name="create_project_htmx",
    ),
    path(
        "htmx/project/<int:project_pk>/delete/",
        views.delete_project_htmx,
        name="delete_project_htmx",
    ),

    # HTMX endpoints для задач
    path(
        "htmx/project/<int:project_pk>/task/create/",
        views.create_task_htmx,
        name="create_task_htmx",
    ),
    path(
        "htmx/task/<int:task_pk>/toggle/",
        views.toggle_task_status,
        name="toggle_task_status",
    ),
    path(
        "htmx/task/<int:task_pk>/edit/",
        views.edit_task_htmx,
        name="edit_task_htmx",
    ),
    path(
        "htmx/task/<int:task_pk>/delete/confirm/",
        views.show_delete_task_modal_htmx,
        name="show_delete_task_modal_htmx",
    ),
    path(
        "htmx/task/<int:task_pk>/delete/",
        views.delete_task_htmx,
        name="delete_task_htmx",
    ),
    path(
        "htmx/project/<int:project_pk>/tasks/reorder/",
        views.reorder_tasks_htmx,
        name="reorder_tasks_htmx",
    ),
]
