from django.db import models

from users.models import User


class Chat(models.Model):
    """Модель чатов."""

    initiator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="started_chats",
        verbose_name="Инициатор",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="participates_in_chats",
        verbose_name="Получатель",
    )
    start_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания чата",
    )

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self):
        return f"{self.initiator} - {self.receiver}"


class Message(models.Model):
    """Модель сообщений."""

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_messages",
        verbose_name="Отправитель",
    )
    text = models.CharField(
        "Текст",
        max_length=200,
        blank=True,
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        verbose_name="Чат",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время отправки",
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.sender} - {self.timestamp}"
