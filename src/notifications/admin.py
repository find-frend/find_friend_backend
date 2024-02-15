from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Админка для уведомлений."""

    list_display = (
        "user",
        "title",
        "text",
        "created_at",
        "is_read",
    )
