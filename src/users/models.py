from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Кастомный UserManager - уникальный ID пользователя - email."""

    def create_user(self, email, password, **extra_fields):
        """Создание и сохранение пользователя с указанным email и паролем."""
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создание и сохранение суперпользователя с email и паролем."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    USER = "user"
    ADMIN = "admin"

    ROLES_CHOISES = (
        (USER, "user"),
        (ADMIN, "admin"),
    )
    username = None
    email = models.EmailField(
        "Электронная почта",
        max_length=254,
        blank=False,
        null=False,
        unique=True,
    )
    first_name = models.CharField(
        "Имя", max_length=158, blank=False, null=False
    )
    last_name = models.CharField(
        "Фамилия", max_length=150, blank=False, null=False
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES_CHOISES,
        default=USER,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    @property
    def is_user(self):
        return self.role == User.USER

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    def __str__(self):
        return self.email


@receiver(pre_save, sender=User)
def auto_is_staff(sender, instance, *args, **kwargs):
    """Авто присвоение флага is_staff пользователям с ролью 'admin'."""
    if instance.role == User.ADMIN:
        instance.is_staff = True
    elif instance.role == User.USER:
        instance.is_staff = False


@receiver(pre_save, sender=User)
def auto_admin_for_superuser(sender, instance, *args, **kwargs):
    """Авто присвоение роли 'admin' суперюзерам."""
    if instance.is_superuser:
        instance.role = User.ADMIN
        instance.is_staff = True
