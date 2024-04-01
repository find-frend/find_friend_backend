from django.db import models

from config.constants import MAX_LENGTH_CHAR, MAX_LENGTH_TEXT
from users.models import User


class Notification(models.Model):
    """Модель Уведомлений."""

    NOTIFICATION_CHOICES = (
        ("FRIEND_REQUEST", "Запрос в друзья"),
        ("FRIEND_REQUEST_ACCEPTED", "Запрос в друзья принят"),
        ("FRIEND_REQUEST_REJECTED", "Запрос в друзья отклонен"),
        # можно добавить мероприятия
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=MAX_LENGTH_TEXT)
    type = models.CharField(
        max_length=MAX_LENGTH_CHAR,
        choices=NOTIFICATION_CHOICES,
        null=True,
        blank=True,
    )
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return (
            f"Уведомления пользователя "
            f"{self.recipient.first_name}: {self.message}"
        )


class NotificationSettings(models.Model):
    """Модель для настройки уведомлений."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_settings"
    )
    receive_notifications = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Настройка уведомления"
        verbose_name_plural = "Настройки уведомлений"

    def __str__(self):
        return f"Настройки уведомлений пользователя {self.user.first_name}"
