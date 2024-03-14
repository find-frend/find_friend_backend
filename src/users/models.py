import os
from datetime import date
from io import BytesIO

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from django_rest_passwordreset.signals import reset_password_token_created
from PIL import Image

from config.constants import messages
from config.settings import (
    MAX_FILE_SIZE,
    MAX_FILE_SIZE_MB,
    MAX_LENGTH_CHAR,
    MAX_LENGTH_DESCRIBE,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_EVENT,
)

from .exceptions import ImageResizeError, ImageSizeError

# from .utils import make_thumbnail
from .validators import validate_birthday

# from typing import Collection


class FriendRequestManager(models.Manager):
    """Менеджер для модели FriendRequest.

    предоставляющий методы для работы с заявками на дружбу.
    """

    def pending_requests(self, user):
        """Возвращает queryset заявок на дружбу.

        ожидающих ответа от указанного пользователя.
        """
        return self.get_queryset().filter(to_user=user, status="Pending")


class City(models.Model):
    """Модель городов."""

    name = models.CharField(
        max_length=MAX_LENGTH_CHAR, verbose_name="Название города", unique=True
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["name"]

    def __str__(self):
        return self.name


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

    MALE = "М"
    FEMALE = "Ж"
    sex_choices = (
        (MALE, "Mужчина"),
        (FEMALE, "Женщина"),
    )

    username = None
    email = models.EmailField(
        "Электронная почта",
        max_length=MAX_LENGTH_EMAIL,
        blank=False,
        null=False,
        unique=True,
    )
    first_name = models.CharField(
        "Имя",
        max_length=MAX_LENGTH_CHAR,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=r"^[а-яА-ЯёЁa-zA-Z]+(\s?\-?[а-яА-ЯёЁa-zA-Z]+){0,5}$",
                message=messages.INVALID_SYMBOLS_MSG,
                code="invalid_user_first_name",
            ),
            MinLengthValidator(limit_value=2),
        ],
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=MAX_LENGTH_CHAR,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=r"^[а-яА-ЯёЁa-zA-Z]+(\s?\-?[а-яА-ЯёЁa-zA-Z]+){0,5}$",
                message=messages.INVALID_SYMBOLS_MSG,
                code="invalid_user_last_name",
            ),
            MinLengthValidator(limit_value=2),
        ],
    )
    birthday = models.DateField(
        "День рождения",
        blank=True,
        null=True,
        validators=[validate_birthday],
    )
    interests = models.ManyToManyField(
        "Interest",
        through="UserInterest",
        blank=True,
        verbose_name="Интересы",
        help_text="Интересы пользователя",
    )
    friends = models.ManyToManyField(
        "self",
        through="Friendship",
        blank=True,
        verbose_name="Друзья",
        help_text="Друзья пользователя",
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Город проживания",
    )
    avatar = models.ImageField(
        "Аватарка",
        blank=True,
        null=True,
        upload_to="images/user/",
    )
    profession = models.CharField(
        "Работа",
        max_length=MAX_LENGTH_EVENT,
        blank=True,
    )
    sex = models.CharField(
        "Пол",
        max_length=1,
        choices=sex_choices,
        blank=True,
        help_text="Введите свой пол",
    )
    purpose = models.CharField(
        "Цель поиска друга",
        max_length=MAX_LENGTH_EVENT,
        blank=True,
    )
    network_nick = models.CharField(
        "Ник в других соц.сетях",
        max_length=MAX_LENGTH_EVENT,
        blank=True,
    )
    additionally = models.TextField(
        "О себе",
        max_length=MAX_LENGTH_DESCRIBE,
        blank=True,
    )
    """
    nickname = models.SlugField(
        "Ник пользователя",
        max_length=MAX_LENGTH_CHAR,
        unique=True,
        blank=True,
        null=True,
    )
    liked_list = models.JSONField(blank=True, default=list)
    character = models.CharField(
        "Характер",
        max_length=MAX_LENGTH_CHAR,
        blank=True,
    )
    """
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def resize_image(image_bytes):
        """Изменение размера изображения с сохранением пропорций."""
        try:
            with Image.open(BytesIO(image_bytes)) as img:
                img.thumbnail((100, 100), Image.LANCZOS)
                output = BytesIO()
                img.save(output, format=img.format)
                return output.getvalue()
        except Exception as e:
            raise ImageResizeError(
                f"Не удалось изменить размер изображения: {str(e)}"
            )

    @staticmethod
    def check_image_size(image_bytes):
        """Проверка размера изображения."""
        image_size_mb = len(image_bytes) / (1024 * 1024)
        if len(image_bytes) > MAX_FILE_SIZE:
            raise ImageSizeError(
                f"Размер файла {image_size_mb:.2f} "
                f"байт превышает допустимый лимит: {MAX_FILE_SIZE_MB} MB."
            )

    def save_resized_image(self, image, filename):
        """Сохранение измененного изображения."""
        content_file = ContentFile(image)
        self.avatar.save(filename, content_file, save=False)

    def save(self, *args, **kwargs):
        """Сохранение аватара заданного размера с проверкой его размера."""
        if self.avatar:
            filename, ext = os.path.splitext(self.avatar.name)
            try:
                with self.avatar.open("rb") as f:
                    image_bytes = f.read()

                resized_image = self.resize_image(image_bytes)
                self.check_image_size(resized_image)
                new_filename = f"{filename}_resized{ext}"
                self.save_resized_image(resized_image, new_filename)

            except ImageSizeError as e:
                raise ValidationError(f"Ошибка размера файла: {e}")
            except ImageResizeError as e:
                raise ValidationError(f"Ошибка при изменении размера: {e}")
            except Exception as e:
                raise ValidationError(f"Неизвестная ошибка: {e}")

        super().save(*args, **kwargs)

    @property
    def max_file_size(self):
        """Максимальный размер файла (в байтах)."""
        return 8 * 1024 * 1024

    def age(self):
        """Вычисление возраста пользователя."""
        if self.birthday:
            today = date.today()
            return (
                today.year
                - self.birthday.year
                - (
                    (today.month, today.day)
                    < (self.birthday.month, self.birthday.day)
                )
            )
        return None

    def friends_count(self):
        """Получение количества друзей пользователя."""
        return self.friends.count()

    def is_blocked(self, user):
        """Проверка нахождения пользователя в черном списке."""
        return Blacklist.objects.filter(blocked_user=self, user=user).exists()


class Interest(models.Model):
    """Модель интересов."""

    name = models.CharField(
        max_length=MAX_LENGTH_CHAR, verbose_name="Название интереса"
    )
    counter = models.PositiveIntegerField(
        default=0, verbose_name="Счётчик популярности интереса"
    )

    class Meta:
        verbose_name = "Интерес"
        verbose_name_plural = "Интересы"
        ordering = ["-counter"]

    def __str__(self):
        return self.name


class UserInterest(models.Model):
    """Модель связи профиля и интересов."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Увеличение значения счетчика интереса."""
        self.interest.counter += 1
        self.interest.save()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "interest",
                ],
                name="unique_user_interest",
            )
        ]
        verbose_name = "Пользователь-интерес"
        verbose_name_plural = "Пользователи-интересы"

    def __str__(self):
        return f"{self.user} - {self.interest}"


def validate_friend(value):
    """Проверка, что друг существует."""
    friend = get_object_or_404(User, id=value)
    if not friend or not friend.is_active:
        raise ValidationError("Указанный друг не существует.")
    return value


def validate_initiator(value):
    """Проверка, что пользователь существует."""
    initiator = get_object_or_404(User, id=value)
    if not initiator or not initiator.is_active:
        raise ValidationError("Указанный пользователь не существует.")
    return value


class FriendRequest(models.Model):
    """Модель заявки на дружбу между пользователями.."""

    STATUS_CHOICES = (
        ("Pending", "В ожидании"),
        ("Accepted", "Принято"),
        ("Declined", "Отклонено"),
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_friend_requests",
        verbose_name="Инициатор",
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_friend_requests",
        verbose_name="Получатель",
    )
    status = models.CharField(
        max_length=MAX_LENGTH_CHAR,
        choices=STATUS_CHOICES,
        default="Pending",
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Создано"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "from_user",
                    "to_user",
                ],
                name="unique_friend",
            )
        ]

        ordering = ["-created_at"]
        verbose_name = "Заявка в друзья"
        verbose_name_plural = "Заявки в друзья"


class Friendship(models.Model):
    """Модель представления дружеской связи между двумя пользователями."""

    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="initiator",
        verbose_name=_("Инициатор"),
    )
    friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friend",
        verbose_name=_("Друг"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["initiator", "friend"], name="unique_friendship"
            )
        ]
        verbose_name = "Друг"
        verbose_name_plural = "Друзья"


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Обработка токенов сброса пароля.

    При создании токена пользователю отправляется email с кодом.
    :sender: View класс, отправивший сигнал
    :instance: Экземпляр View класса, отправивший сигнал
    :reset_password_token: Объект модели токена
    :args: Позиционные аргументы
    :kwargs: Именованные аргументы
    :return: None
    """
    email_plaintext_message = "Ваш код для восстановления пароля: {}".format(
        reset_password_token.key
    )

    send_mail(
        # Тема:
        "Восстановление пароля",
        # Сообщение:
        email_plaintext_message,
        # Отправитель:
        "noreply@somehost.local",
        # Почта получателя:
        [reset_password_token.user.email],
    )


class Blacklist(models.Model):
    """Модель хранения черного списка пользователей."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blocker",
        verbose_name="Пользователь",
    )
    blocked_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blocked",
        verbose_name="Блокирован",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "user",
                    "blocked_user",
                ),
                name="Unique_Blacklist",
            )
        ]
        verbose_name = "Черный список"
        verbose_name_plural = "Черные списки"

    def clean(self):
        """Валидация блокировки себя."""
        if self.user == self.blocked_user:
            raise ValidationError("Пользователь не может блокировать себя.")

    def save(self, *args, **kwargs):
        """Кастомный save."""
        self.full_clean()
        return super().save(*args, **kwargs)
