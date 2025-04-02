from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=255)

    money_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Баланс"
    )

    token_version = models.IntegerField(default=1)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    objects = UserManager()

    last_login = None
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.login

    @property
    def is_active(self):
        return True

    def get_last_login(self):
        return None

    def set_last_login(self, value):
        pass
