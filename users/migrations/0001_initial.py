# Generated by Django 4.2.20 on 2025-04-01 15:42

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(db_index=True, max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('money_balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Баланс')),
                ('token_version', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
