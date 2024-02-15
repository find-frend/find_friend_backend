from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Notification(models.Model):
    """Модель уводемдений."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=156,)
    text = models.TextField(max_length=256,)
    created_at = models.DateTimeField(auto_now_add=True,)
    is_read = models.BooleanField(default=False,)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
