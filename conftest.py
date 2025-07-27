import pytest


@pytest.fixture
def user():
    """Створення тестового користувача"""
    from django.contrib.auth.models import User

    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def another_user():
    """Створення другого тестового користувача"""
    from django.contrib.auth.models import User

    return User.objects.create_user(
        username="anotheruser",
        email="another@example.com",
        password="testpass123",
    )
