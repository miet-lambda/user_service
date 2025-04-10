from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Название проекта",
        help_text="Введите название проекта"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        null=False,
        blank=False,
        verbose_name="Владелец",
        help_text="Выберите владельца проекта"
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class Script(models.Model):
    path = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Путь к скрипту",
        help_text="Укажите относительный путь к скрипту"
    )
    source_code = models.TextField(
        null=False,
        blank=False,
        verbose_name="Исходный код",
        help_text="Введите исходный код скрипта"
    )
    parent_project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="scripts",
        null=False,
        blank=False,
        verbose_name="Родительский проект",
        help_text="Выберите проект, к которому относится скрипт"
    )

    class Meta:
        verbose_name = "Скрипт"
        verbose_name_plural = "Скрипты"
        ordering = ["id"]
        unique_together = [["parent_project", "path"]]

    def __str__(self):
        return f"{self.path} (Проект: {self.parent_project.name})"
