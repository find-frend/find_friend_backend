import logging

from django.apps import apps


def send_notification(recipient, notification_type, message):
    """Отправляет уведомление получателю."""
    try:
        notifications = apps.get_model("notifications", "Notification")
        notification = notifications.objects.create(
            recipient=recipient,
            type=notification_type,
            message=message,
        )
        logging.info(
            f"Уведомления отправлено: Получатель - {recipient}, "
            f"Тип уведомления - {notification_type}, Сообщение - {message}")
        return notification
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")


def handle_friend_request(instance):
    """Обрабатывает запрос на добавление в друзья."""
    notification_settings = apps.get_model("notifications",
                                           "NotificationSettings")
    try:
        recipient_settings = notification_settings.objects.get(
            user=instance.from_user)
        if recipient_settings.receive_notifications:
            if instance.status == "Accepted":
                message = (f"{instance.to_user} принял Ваш "
                           f"запрос на добавления в друзья.")
                notification_type = "FRIEND_REQUEST_ACCEPTED"
                send_notification(instance.from_user, notification_type,
                                  message)
            elif instance.status == "Declined":
                message = (f"{instance.to_user} отклонил Ваш запрос на "
                           f"добавления в друзья.")
                notification_type = "FRIEND_REQUEST_REJECTED"
                send_notification(instance.from_user, notification_type,
                                  message)
    except notification_settings.DoesNotExist:
        logging.error("Настройки уведомлений для пользователя не найдены.")
