import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date, timedelta

from tasks.models import Project, Task


@pytest.mark.django_db
class TestCRUDOperations:
    """Тести CRUD операцій"""

    def test_create_update_delete_projects(self, authenticated_client, user):
        # CREATE - створюємо проєкт
        response = authenticated_client.post(
            reverse('tasks:create_project_htmx'),
            {'name': 'New Project'}
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'HX-Redirect' in response.headers

        # Перевіряємо що проєкт створився
        project = Project.objects.get(name='New Project', user=user)
        assert project.name == 'New Project'

        # READ - читаємо проєкт
        response = authenticated_client.get(
            reverse('tasks:project_detail', kwargs={'pk': project.pk})
        )
        assert response.status_code == status.HTTP_200_OK
        assert b'New Project' in response.content

        # DELETE - видаляємо проєкт
        response = authenticated_client.delete(
            reverse('tasks:delete_project_htmx',
                    kwargs={'project_pk': project.pk})
        )
        assert response.status_code == status.HTTP_200_OK

        # Перевіряємо що проєкт видалився
        assert not Project.objects.filter(pk=project.pk).exists()

    def test_add_update_delete_tasks(self, authenticated_client, project):
        # ADD - додаємо задачу
        response = authenticated_client.post(
            reverse('tasks:create_task_htmx',
                    kwargs={'project_pk': project.pk}),
            {
                'name': 'New Task',
                'priority': 'high',
                'status': 'pending'
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert b'New Task' in response.content

        # Перевіряємо що задача створилась
        task = Task.objects.get(name='New Task', project=project)
        assert task.priority == 'high'
        assert task.status == 'pending'

        # UPDATE - оновлюємо задачу
        response = authenticated_client.post(
            reverse('tasks:edit_task_htmx', kwargs={'task_pk': task.pk}),
            {
                'name': 'Updated Task',
                'priority': 'low',
                'status': 'in_progress'
            }
        )
        assert response.status_code == status.HTTP_200_OK

        # Перевіряємо що задача оновилась
        task.refresh_from_db()
        assert task.name == 'Updated Task'
        assert task.priority == 'low'

        # DELETE - видаляємо задачу
        response = authenticated_client.delete(
            reverse('tasks:delete_task_htmx', kwargs={'task_pk': task.pk})
        )
        assert response.status_code == status.HTTP_200_OK

        # Перевіряємо що задача видалилась
        assert not Task.objects.filter(pk=task.pk).exists()

    def test_mark_task_as_done(self, authenticated_client, task):
        """Тестуємо позначення задачі як виконаної"""

        # Початковий статус має бути pending
        assert task.status == 'pending'

        # Перемикаємо статус на completed
        response = authenticated_client.get(
            reverse('tasks:toggle_task_status', kwargs={'task_pk': task.pk})
        )
        assert response.status_code == status.HTTP_200_OK

        # Перевіряємо що статус змінився на completed
        task.refresh_from_db()
        assert task.status == 'completed'

        # Перемикаємо назад на pending
        response = authenticated_client.get(
            reverse('tasks:toggle_task_status', kwargs={'task_pk': task.pk})
        )
        assert response.status_code == status.HTTP_200_OK

        # Перевіряємо що статус повернувся до pending
        task.refresh_from_db()
        assert task.status == 'pending'
