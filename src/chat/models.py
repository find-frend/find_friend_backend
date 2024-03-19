from django.db import models

from users.models import User


class Chat(models.Model):
    """Модель чатов."""

    initiator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="started_chats",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="participates_in_chats",
    )
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.initiator} - {self.receiver}"


class Message(models.Model):
    """Модель сообщений."""

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="message_sender",
    )
    text = models.CharField(max_length=200, blank=True)
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="chat_messages",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.timestamp}"

    class Meta:
        ordering = ("-timestamp",)
