from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import DetailView, ListView

from tasks.forms import ProjectForm, TaskForm
from tasks.models import Project, Task


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "tasks/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = TaskForm()
        return context


# HTMX Views для AJAX операцій

@login_required
@require_POST
def create_project_htmx(request):
    """HTMX: Створення нового проєкту через модальне вікно"""
    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save(commit=False)
        project.user = request.user
        project.save()
        # Після успішного створення перенаправляємо на сторінку проєкту
        response = HttpResponse()
        response['HX-Redirect'] = f'/project/{project.pk}/'
        return response
    else:
        return render(request, 'tasks/partials/project_create_modal.html',
                      {'form': form})


@login_required
@require_POST
def create_task_htmx(request, project_pk):
    """HTMX: Створення нової задачі"""
    project = get_object_or_404(Project, pk=project_pk, user=request.user)
    form = TaskForm(request.POST)

    if form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()
        return render(request, 'tasks/partials/task_item.html',
                      {'task': task})
    else:
        return render(request, 'tasks/partials/task_form_errors.html',
                      {'form': form})


@login_required
def toggle_task_status(request, task_pk):
    """HTMX: Зміна статусу задачі (completed/pending)"""
    task = get_object_or_404(Task, pk=task_pk, project__user=request.user)

    # Перемикаємо статус
    if task.status == 'completed':
        task.status = 'pending'
    else:
        task.status = 'completed'
    task.save()

    return render(request, 'tasks/partials/task_item.html',
                  {'task': task})


@login_required
@require_http_methods(['DELETE', 'POST'])
def delete_task_htmx(request, task_pk):
    """HTMX: Видалення задачі"""
    task = get_object_or_404(Task, pk=task_pk, project__user=request.user)
    task.delete()
    return HttpResponse('')


@login_required
def edit_task_htmx(request, task_pk):
    """HTMX: Редагування задачі"""
    task = get_object_or_404(Task, pk=task_pk, project__user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return render(request, 'tasks/partials/task_item.html',
                          {'task': task})
        else:
            return render(request, 'tasks/partials/task_edit_form.html',
                          {'form': form, 'task': task})
    else:
        # GET запит - показуємо форму редагування або скасовуємо
        if request.GET.get('cancel'):
            return render(request, 'tasks/partials/task_item.html', {'task': task})
        else:
            form = TaskForm(instance=task)
            return render(request, 'tasks/partials/task_edit_form.html',
                          {'form': form, 'task': task})


@login_required
def delete_project_htmx(request, project_pk):
    """HTMX: Видалення проєкту"""
    project = get_object_or_404(Project, pk=project_pk, user=request.user)
    project.delete()
    return HttpResponse('')


@login_required
def show_project_form_htmx(request):
    """HTMX: Показати форму створення проєкту в модальному вікні"""
    form = ProjectForm()
    return render(request, 'tasks/partials/project_create_modal.html',
                  {'form': form})


@login_required
def show_delete_task_modal_htmx(request, task_pk):
    """HTMX: Показати модальне вікно підтвердження видалення задачі"""
    task = get_object_or_404(Task, pk=task_pk, project__user=request.user)
    return render(request, 'tasks/partials/task_delete_modal.html',
                  {'task': task})


def home_redirect(request):
    """Розумна навігація з головної сторінки"""
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    user_projects = request.user.projects.all()

    if user_projects.exists():
        # Якщо є проєкти - редірект на перший
        first_project = user_projects.first()
        return redirect('tasks:project_detail', pk=first_project.pk)
    else:
        # Якщо немає проєктів - створюємо перший
        from tasks.models import Project
        default_project = Project.objects.create(
            name="My Tasks",
            user=request.user
        )
        return redirect('tasks:project_detail', pk=default_project.pk)


@login_required
@require_POST
def reorder_tasks_htmx(request, project_pk):
    """HTMX: Оновлення порядку задач після drag & drop"""
    project = get_object_or_404(Project, pk=project_pk, user=request.user)

    task_ids = request.POST.getlist('task_ids[]')

    for index, task_id in enumerate(task_ids):
        Task.objects.filter(
            pk=task_id,
            project=project
        ).update(order=index + 1)

    tasks = project.tasks.all()
    return render(request, 'tasks/partials/task_list.html',
                  {'tasks': tasks})
