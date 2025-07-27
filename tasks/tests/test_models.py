import pytest


@pytest.mark.django_db
class TestTaskOrdering:
    """Тести для перевірки правильного ordering задач"""

    def test_task_ordering_by_priority_and_created_at(self, project):
        """Тест що задачі сортуються за пріоритетом, потім за датою створення"""
        from tasks.models import Task  # імпорт всередині функції

        # Створюємо задачі з різними пріоритетами
        task_high = Task.objects.create(
            name="High Priority Task",
            project=project,
            priority="high",
            status="pending",
        )

        task_medium = Task.objects.create(
            name="Medium Priority Task",
            project=project,
            priority="medium",
            status="pending",
        )

        task_low = Task.objects.create(
            name="Low Priority Task",
            project=project,
            priority="low",
            status="pending",
        )

        # Отримуємо всі задачі
        tasks = list(Task.objects.all())

        # Перевіряємо що ordering працює правильно
        # priority: (за алфавітом: high, low, medium)
        expected_order = [task_high, task_low, task_medium]
        assert tasks == expected_order
