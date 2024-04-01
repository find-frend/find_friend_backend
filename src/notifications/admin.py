from django.contrib import admin

from .models import Notification, NotificationSettings


@admin.register(Notification)
class Notification(admin.ModelAdmin):
    """Админка для модели Notification."""
    list_display = ("recipient", "message", "type", "created_at", "read")


@admin.register(NotificationSettings)
class NotificationSettings(admin.ModelAdmin):
    """Админка для модели NotificationSettings."""
    list_display = ("user", "receive_notifications",)
