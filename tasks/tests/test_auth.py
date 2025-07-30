import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

from tasks.models import Project, Task


@pytest.mark.django_db
class TestAuthentication:
    def test_unauthenticated_user_redirected_to_login(self):
        """Неавторизований користувач перенаправляється на login"""
        client = Client()

        user = User.objects.create_user(username='testuser',
                                        password='pass123')
        project = Project.objects.create(name='Test Project', user=user)

        # Пробуємо доступитися до project detail без авторизації
        response = client.get(reverse('tasks:project_detail',
                                      kwargs={'pk': project.pk}))

        # Має перенаправити на login
        assert response.status_code == status.HTTP_302_FOUND
        assert '/accounts/login/' in response.url


@pytest.mark.django_db
class TestAuthorization:
    def test_user_cannot_see_other_users_projects(self,
                                                  authenticated_client, user):
        """Користувач не може бачити чужі проєкти"""
        other_user = User.objects.create_user(username='otheruser',
                                              password='pass123')
        other_project = Project.objects.create(name='Other Project',
                                               user=other_user)

        # Пробуємо доступитися до чужого проєкту
        response = authenticated_client.get(
            reverse('tasks:project_detail', kwargs={'pk': other_project.pk})
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_cannot_edit_other_users_tasks(self,
                                                authenticated_client, user):
        # Створюємо іншого користувача, його проєкт і задачу
        other_user = User.objects.create_user(username='otheruser',
                                              password='pass123')
        other_project = Project.objects.create(name='Other Project',
                                               user=other_user)
        other_task = Task.objects.create(
            name='Other Task',
            project=other_project,
            status='pending',
            priority='medium'
        )

        # Пробуємо редагувати чужу задачу
        response = authenticated_client.post(
            reverse('tasks:edit_task_htmx', kwargs={'task_pk': other_task.pk}),
            {'name': 'Hacked Task', 'priority': 'high', 'status': 'pending'}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Перевіряємо що задача не змінилась
        other_task.refresh_from_db()
        assert other_task.name == 'Other Task'
