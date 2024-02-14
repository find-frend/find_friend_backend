from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings import MAX_LENGTH_CHAR, MAX_LENGTH_EMAIL

from .utils import make_thumbnail


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

    username = None
    email = models.EmailField(
        "Электронная почта",
        max_length=MAX_LENGTH_EMAIL,
        blank=False,
        null=False,
        unique=True,
    )
    first_name = models.CharField(
        "Имя", max_length=MAX_LENGTH_CHAR, blank=False, null=False
    )
    last_name = models.CharField(
        "Фамилия", max_length=MAX_LENGTH_CHAR, blank=False, null=False
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    """Модель профиля пользователя."""

    MALE = "М"
    FEMALE = "Ж"
    sex_choices = (
        (MALE, "Mужчина"),
        (FEMALE, "Женщина"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
    )
    # primary_key=True,)
    email = models.EmailField(
        _("Электронная почта"), max_length=MAX_LENGTH_EMAIL, unique=True
    )
    last_name = models.CharField(
        _("Фамилия"),
        max_length=MAX_LENGTH_CHAR,
        null=True,
    )
    first_name = models.CharField(
        _("Имя"),
        max_length=MAX_LENGTH_CHAR,
        null=True,
    )
    nickname = models.SlugField(
        "Ник пользователя",
        max_length=MAX_LENGTH_CHAR,
        unique=True,
        blank=True,
        null=True,
    )
    age = models.PositiveIntegerField(
        "Возраст",
        blank=True,
        null=True,
    )
    interests = models.JSONField("Интересы", blank=False, default=list)
    city = models.CharField(
        "Место проживания",
        max_length=MAX_LENGTH_CHAR,
        null=True,
        blank=True,
    )
    liked_list = models.JSONField(blank=True, default=list)
    avatar = models.ImageField(
        "Аватарка",
        null=True,
        blank=True,
        default="",
        upload_to="images/profile/",
    )
    profession = models.CharField(
        "Профессия",
        max_length=MAX_LENGTH_CHAR,
        blank=True,
    )
    character = models.CharField(
        "Характер",
        max_length=MAX_LENGTH_CHAR,
        blank=True,
    )
    sex = models.CharField(
        "Пол",
        max_length=1,
        choices=sex_choices,
        default=FEMALE,
        help_text="Введите свой пол",
    )
    purpose = models.CharField(
        "Цель поиска друга",
        max_length=MAX_LENGTH_CHAR,
        null=True,
        blank=True,
    )
    network_nick = models.CharField(
        "Ник в других соц.сетях",
        max_length=MAX_LENGTH_CHAR,
        null=True,
        blank=True,
    )
    additionally = models.TextField(
        "Дополнительно",
        max_length=MAX_LENGTH_CHAR,
        blank=True,
    )
    USERNAME_FIELD = "nickname"
    REQUIRED_FIELDS = [interests]

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        """Сохранение аватара заданного размера."""
        self.avatar = make_thumbnail(self.avatar, size=(100, 100))
        super().save(*args, **kwargs)


class Friend(models.Model):
    """Модель друзей."""
    initiator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="initiator"
    )
    friend = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend"
    )
    is_added = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "application_creator",
                    "friend",
                ],
                name="unique_friend",
            )
        ]
        verbose_name = "Друг"
        verbose_name_plural = "Друзья"

    def __str__(self):
        return f"{self.friend} в друзьях у {self.initiator}"
