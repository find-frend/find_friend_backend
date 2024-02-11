from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

USER = 'user'
ADMIN = 'admin'


class User(AbstractUser):
    """Модель пользователя."""

    ROLES_CHOISES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(
        'Логин',
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        validators=[RegexValidator(regex='^[\\w.@+-]+\\Z',
                                   message='Набор символов неверный')])
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        blank=False,
        null=False,
        unique=True)
    first_name = models.CharField(
        'Имя пользователя',
        max_length=158,
        blank=False,
        null=False)
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        blank=False,
        null=False)
    role = models.CharField(
        max_length=20,
        choices=ROLES_CHOISES,
        default='user',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models. UniqueConstraint(
                fields=['username', 'email'],
                name='unique_constraint'
            ),
        ]

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    def __str__(self):
        return self.username
