from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import ModelSerializer

from events.models import Event
from notifications.models import Notification
from users.models import Friend, Profile, User


class MyUserSerializer(UserSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            "password",
        )


class ProfileSerializer(ModelSerializer):
    """Сериализатор профиля пользователя."""

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "email",
            "nickname",
            "age",
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


class NotificationSerializer(ModelSerializer):
    """Сериализатор уведомлений."""

    class Meta:
        model = Notification
        fields = "__all__"
