from django.db.models import Q
from django.shortcuts import redirect, reverse
from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chat.models import Chat
from chat.serializers import ChatListSerializer, ChatSerializer
from config.constants import messages
from users.models import Friendship, User


@api_view(["POST"])
def start_chat(request):
    """Открытие нового чата."""
    data = request.data
    email = data.get("email")
    try:
        participant = User.objects.get(email=email)
    except User.DoesNotExist:
        raise exceptions.NotFound(
            detail=messages.CANNOT_START_CHAT_WITH_NONEXISTENT_USER
        )

    # Проверяем, что пользователь, с которым мы начинаем чат, у нас в друзьях
    if not (
        Friendship.objects.filter(
            Q(initiator=request.user, friend=participant)
            | Q(initiator=participant, friend=request.user),
        ).exists()
    ):
        raise exceptions.ValidationError(
            detail=messages.USER_IS_NOT_FRIEND % str(participant)
        )

    # Если чат между пользователями уже существует, переадресуем на него
    chat = Chat.objects.filter(
        Q(initiator=request.user, receiver=participant)
        | Q(initiator=participant, receiver=request.user)
    )
    if chat.exists():
        return redirect(reverse("api:chat:get_chat", args=(chat[0].id,)))

    # Если чат еще не существует, создаем его
    chat = Chat.objects.create(initiator=request.user, receiver=participant)
    return Response(ChatSerializer(instance=chat).data)


@api_view(["GET"])
def get_chat(request, chat_id):
    """Просмотр чата."""
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        raise exceptions.NotFound(detail=messages.CHAT_DOES_NOT_EXIST)

    # Проверяем права доступа к чату
    if not any(
        (
            request.user.is_staff,
            request.user == chat.initiator,
            request.user == chat.receiver,
        )
    ):
        raise exceptions.PermissionDenied(
            detail=messages.USER_NOT_ALLOWED_TO_VIEW_CHAT
        )
    return Response(ChatSerializer(instance=chat).data)


@api_view(["GET"])
def chats(request):
    """Список чатов."""
    chat_list = Chat.objects.filter(
        Q(initiator=request.user) | Q(receiver=request.user)
    )
    serializer = ChatListSerializer(instance=chat_list, many=True)
    return Response(serializer.data)
