from datetime import date, timedelta

import pytest
from django.test import Client

from tasks.models import Project, Task


@pytest.fixture
def authenticated_client(user):
    """Django test client з автентифікованим користувачем"""

    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def project(user):
    """Створення тестового проєкту"""

    return Project.objects.create(name="Test Project", user=user)


@pytest.fixture
def task(project):
    """Створення тестової задачі"""

    return Task.objects.create(
        name="Test Task",
        project=project,
        status="pending",
        priority="medium",
        deadline=date.today() + timedelta(days=7),
    )


@pytest.fixture
def multiple_tasks(project):
    """Створення декількох задач для тестування списків"""

    tasks = []
    for i in range(3):
        task = Task.objects.create(
            name=f"Task {i+1}",
            project=project,
            status="pending",
            priority="low",
            order=i+1
        )
        tasks.append(task)
    return tasks