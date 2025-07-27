from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from tasks.models import Project, Task


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "tasks/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "tasks/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
