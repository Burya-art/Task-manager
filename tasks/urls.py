from django.urls import path

from tasks import views

app_name = "tasks"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project_list"),
    path(
        "project/<int:pk>/",
        views.ProjectDetailView.as_view(),
        name="project_detail",
    ),
]
