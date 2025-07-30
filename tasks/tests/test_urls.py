import pytest
from django.urls import reverse
from rest_framework import status

from tasks.models import Project, Task


@pytest.mark.django_db
class TestTasksEndpoints:
    """Integration tests for endpoints"""

    def test_project_detail_endpoint(self, authenticated_client, project):
        response = authenticated_client.get(
            reverse('tasks:project_detail', kwargs={'pk': project.pk}))

        assert response.status_code == status.HTTP_200_OK
        assert b'Test Project' in response.content
        assert 'tasks/project_detail.html' in \
               [t.name for t in response.templates]

    def test_show_project_creation_form_htmx_endpoint(
            self, authenticated_client):
        response = authenticated_client.get(
            reverse('tasks:show_project_form_htmx'))

        assert response.status_code == status.HTTP_200_OK
        assert 'tasks/partials/project_create_modal.html' in \
               [t.name for t in response.templates]

    def test_create_project_htmx_endpoint(self, authenticated_client, user):
        response = authenticated_client.post(
            reverse('tasks:create_project_htmx'), {'name': 'New Test Project'})

        assert response.status_code == status.HTTP_200_OK
        assert 'HX-Redirect' in response.headers
        assert Project.objects.filter(name='New Test Project', user=user).exists()

    def test_delete_project_htmx_endpoint(self, authenticated_client, project):
        response = authenticated_client.delete(
            reverse('tasks:delete_project_htmx', kwargs={'project_pk': project.pk}))

        assert response.status_code == status.HTTP_200_OK
        assert not Project.objects.filter(pk=project.pk).exists()

    def test_create_task_htmx_endpoint(self, authenticated_client, project):
        response = authenticated_client.post(
            reverse('tasks:create_task_htmx', kwargs={'project_pk': project.pk}), {
                'name': 'New Task',
                'priority': 'medium',
                'status': 'pending'
            })

        assert response.status_code == status.HTTP_200_OK
        assert b'New Task' in response.content
        assert Task.objects.filter(name='New Task', project=project).exists()

    def test_toggle_task_status_endpoint(self, authenticated_client, task):
        initial_status = task.status

        response = authenticated_client.get(
            reverse('tasks:toggle_task_status', kwargs={'task_pk': task.pk}))

        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        expected_status = 'completed' if initial_status == 'pending' else 'pending'
        assert task.status == expected_status

    def test_edit_task_htmx_endpoint_get(self, authenticated_client, task):
        response = authenticated_client.get(
            reverse('tasks:edit_task_htmx', kwargs={'task_pk': task.pk}))

        assert response.status_code == status.HTTP_200_OK
        assert b'Test Task' in response.content
        assert 'tasks/partials/task_edit_form.html' in [t.name for t in response.templates]

    def test_edit_task_htmx_endpoint_post(self, authenticated_client, task):
        response = authenticated_client.post(
            reverse('tasks:edit_task_htmx', kwargs={'task_pk': task.pk}), {
                'name': 'Updated Task Name',
                'priority': 'high',
                'status': 'in_progress'
            })

        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.name == 'Updated Task Name'
        assert task.priority == 'high'

    def test_show_delete_task_modal_htmx_endpoint(
            self, authenticated_client, task):
        response = authenticated_client.get(
            reverse('tasks:show_delete_task_modal_htmx',
                    kwargs={'task_pk': task.pk}))

        assert response.status_code == status.HTTP_200_OK
        assert 'tasks/partials/task_delete_modal.html' in \
               [t.name for t in response.templates]

    def test_delete_task_htmx_endpoint(self, authenticated_client, task):
        response = authenticated_client.delete(
            reverse('tasks:delete_task_htmx', kwargs={'task_pk': task.pk}))

        assert response.status_code == status.HTTP_200_OK
        assert response.content == b''
        assert not Task.objects.filter(pk=task.pk).exists()

    def test_reorder_tasks_htmx_endpoint(
            self, authenticated_client, project, multiple_tasks):
        task_ids = [str(task.pk) for task in reversed(multiple_tasks)]

        response = authenticated_client.post(
            reverse('tasks:reorder_tasks_htmx',
                    kwargs={'project_pk': project.pk}),
            {'task_ids[]': task_ids})

        assert response.status_code == status.HTTP_200_OK
        reordered_tasks = Task.objects.filter(project=project).order_by('order')
        assert list(reordered_tasks.values_list('pk', flat=True)) == \
               [int(id) for id in task_ids]
