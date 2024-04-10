from django.db.models import Q
from rest_framework import exceptions

from chat.models import Chat
from config.constants import messages
from users.models import Friendship


def get_chat_and_permissions(user, chat_id):
    """Проверка прав доступа пользователя к чату."""
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        raise exceptions.NotFound(detail=messages.CHAT_DOES_NOT_EXIST)

    if not any(
        (
            user.is_staff,
            user == chat.initiator,
            user == chat.receiver,
        )
    ):
        raise exceptions.PermissionDenied(
            detail=messages.USER_NOT_ALLOWED_TO_VIEW_CHAT
        )

    return chat


def check_friendshhip(user, other_user):
    """Проверка дружбы между пользователями."""
    qs = Friendship.objects.filter(
        Q(initiator=user, friend=other_user)
        | Q(initiator=other_user, friend=user),
    )
    if not qs.exists():
        raise exceptions.PermissionDenied(
            detail=messages.USER_IS_NOT_FRIEND % str(other_user)
        )
    return qs.first()
