import pytest
from django.urls import reverse
from rest_framework import status

from tasks.models import Project, Task


@pytest.mark.django_db
class TestValidation:
    def test_project_name_too_short_rejected(self, authenticated_client, user):
        """Менше 3 символів відхиляється"""

        response = authenticated_client.post(
            reverse('tasks:create_project_htmx'),
            {'name': 'AB'}
        )

        # Має відхилити (не redirect)
        assert 'HX-Redirect' not in response.headers
        # Проєкт не створюється
        assert not Project.objects.filter(name='AB', user=user).exists()

    def test_task_name_too_short_rejected(self, authenticated_client, project):
        """Коротке ім'я задачі (менше 3 символів) відхиляється"""

        response = authenticated_client.post(
            reverse('tasks:create_task_htmx', kwargs={'project_pk': project.pk}),
            {'name': 'XY', 'priority': 'medium', 'status': 'pending'}
        )

        # Задача не створюється
        assert not Task.objects.filter(name='XY', project=project).exists()

    def test_empty_project_name_rejected(self, authenticated_client, user):
        """Порожнє ім'я проєкту відхиляється"""

        response = authenticated_client.post(
            reverse('tasks:create_project_htmx'),
            {'name': ''}
        )

        assert not Project.objects.filter(name='', user=user).exists()

    def test_empty_task_name_rejected(self, authenticated_client, project):
        """Порожнє ім'я задачі відхиляється"""

        response = authenticated_client.post(
            reverse('tasks:create_task_htmx', kwargs={'project_pk': project.pk}),
            {'name': '', 'priority': 'medium', 'status': 'pending'}  # Порожнє
        )

        assert not Task.objects.filter(name='', project=project).exists()
