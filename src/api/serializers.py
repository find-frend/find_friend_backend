from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import ModelSerializer

from events.models import Event
from users.models import Friend, User


class MyUserSerializer(UserSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "nickname",
            "birthday",
            "interests",
            "city",
            "avatar",
            "profession",
            "character",
            "sex",
            "purpose",
            "network_nick",
            "additionally",
        )


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            "password",
        )


class FriendSerializer(ModelSerializer):
    """Сериализатор друга пользователя."""

    class Meta:
        model = Friend
        fields = (
            "id",
            "initiator",
            "friend",
            "is_added",
        )


class EventSerializer(ModelSerializer):
    """Сериализатор мероприятия пользователя."""

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "interests",
            "event_type",
            "date",
            "location",
            "image",
        )
