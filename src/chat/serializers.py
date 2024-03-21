from rest_framework import serializers

from api.serializers import MyUserGetSerializer

# from users.models import User
from config.settings import MAX_MESSAGES_IN_CHAT

from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщений."""

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "text",
            "timestamp",
        )


class ChatListSerializer(serializers.ModelSerializer):
    """Сериализатор списка чатов."""

    initiator = MyUserGetSerializer()
    receiver = MyUserGetSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = (
            "id",
            "initiator",
            "receiver",
            "start_time",
            "last_message",
        )

    def get_last_message(self, instance):
        """Получение последнего сообщения в чате."""
        last_message = (
            Message.objects.filter(chat=instance)
            .order_by("-timestamp")
            .first()
        )
        if last_message:
            return MessageSerializer(instance=last_message).data
        return None


class ChatSerializer(serializers.ModelSerializer):
    """Сериализатор чата."""

    initiator = MyUserGetSerializer(read_only=True)
    receiver = MyUserGetSerializer(read_only=True)
    email = serializers.CharField(write_only=True)
    chat_messages = serializers.SerializerMethodField(
        "get_limited_chat_messages"
    )

    class Meta:
        model = Chat
        fields = (
            "id",
            "initiator",
            "receiver",
            "email",
            "chat_messages",
        )

    def get_limited_chat_messages(self, obj):
        """Получение ограниченного количества сообщений в чате."""
        qs = obj.chat_messages.all()[:MAX_MESSAGES_IN_CHAT]
        return MessageSerializer(instance=qs, many=True).data
