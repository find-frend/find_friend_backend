from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import ModelSerializer

from users.models import Profile, User


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
