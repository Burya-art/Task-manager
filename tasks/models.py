from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Проєкт"
        verbose_name_plural = "Проєкти"
        ordering = ["-created_at"]
        db_table = "projects"

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Очікує"),
        ("in_progress", "В роботі"),
        ("completed", "Завершено"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Низький"),
        ("medium", "Середній"),
        ("high", "Високий"),
    ]

    name = models.CharField(max_length=200)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачі"
        ordering = ["priority", "-created_at"]
        db_table = "tasks"

    def __str__(self):
        return self.name
