import pytest
from datetime import date, timedelta


@pytest.fixture
def project(user):
    """Створення тестового проєкту"""
    from tasks.models import Project

    return Project.objects.create(name="Test Project", user=user)


@pytest.fixture
def task(project):
    """Створення тестової задачі"""
    from tasks.models import Task

    return Task.objects.create(
        name="Test Task",
        project=project,
        status="pending",
        priority="medium",
        deadline=date.today() + timedelta(days=7),
    )
