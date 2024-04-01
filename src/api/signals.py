import logging

from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import handle_friend_request, send_notification


@receiver(post_save, sender="users.User")
def create_notification_settings(sender, instance, created, **kwargs):
    """Создает настройки уведомлений при создании пользователя."""
    notification_settings = apps.get_model("notifications",
                                           "NotificationSettings")
    if created:
        notification_settings.objects.create(user=instance)


@receiver(post_save, sender="users.FriendRequest")
def friend_request_notification(sender, instance, created, **kwargs):
    """Отправляет уведомление о запросе на добавление в друзья."""
    notification_settings = apps.get_model("notifications",
                                           "NotificationSettings")
    if created:
        try:
            recipient_settings = notification_settings.objects.get(
                user=instance.to_user)
            if recipient_settings.receive_notifications:
                message = (f"{instance.from_user} отправил "
                           f"Вам запрос на добавления в друзья.")
                notification_type = "FRIEND_REQUEST"
                send_notification(instance.to_user, notification_type, message)
        except notification_settings.DoesNotExist:
            logging.error(
                "Настройки уведомлений не найдены для получателя.")
    else:
        handle_friend_request(instance)


@receiver(post_save, sender="users.FriendRequest")
def create_friendship(sender, instance, created, **kwargs):
    """Создает объект Friendship после принятия заявки на дружбу."""
    from users.models import Friendship

    if instance.status == "Accepted":
        Friendship.objects.get_or_create(
            initiator=instance.from_user, friend=instance.to_user
        )
