from django.db import models

from users.models import User


class Chat(models.Model):
    """Модель чатов."""

    initiator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="chat_starter",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="chat_participant",
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
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.timestamp}"

    class Meta:
        ordering = ("-timestamp",)
