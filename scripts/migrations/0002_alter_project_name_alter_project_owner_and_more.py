# Generated by Django 4.2.20 on 2025-04-09 22:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scripts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(help_text='Введите название проекта', max_length=255, verbose_name='Название проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(help_text='Выберите владельца проекта', on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='script',
            name='parent_project',
            field=models.ForeignKey(help_text='Выберите проект, к которому относится скрипт', on_delete=django.db.models.deletion.CASCADE, related_name='scripts', to='scripts.project', verbose_name='Родительский проект'),
        ),
        migrations.AlterField(
            model_name='script',
            name='path',
            field=models.CharField(help_text='Укажите относительный путь к скрипту', max_length=255, verbose_name='Путь к скрипту'),
        ),
        migrations.AlterField(
            model_name='script',
            name='source_code',
            field=models.TextField(help_text='Введите исходный код скрипта', verbose_name='Исходный код'),
        ),
    ]
