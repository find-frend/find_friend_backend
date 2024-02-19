from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import ModelSerializer

from events.models import Event, EventInterest
from users.models import Friend, Interest, User, UserInterest


class InterestSerializer(ModelSerializer):
    """Сериализатор интересов."""

    class Meta:
        model = Interest
        fields = ("id", "name")


class MyUserSerializer(UserSerializer):
    """Сериализатор пользователя."""

    interests = InterestSerializer(many=True)

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

    def create(self, validated_data):
        """Создание пользователя с указанными интересами."""
        if "interests" not in self.initial_data:
            return User.objects.create(**validated_data)
        interests = validated_data.pop("interests")
        user = User.objects.create(**validated_data)
        for interest in interests:
            current_interest = Interest.objects.get(**interest)
            UserInterest.objects.create(user=user, interest=current_interest)
        return user

    def update(self, instance, validated_data):
        """Обновление пользователя с указанными интересами."""
        if "interests" not in self.initial_data:
            return super().update(instance, validated_data)
        interests = validated_data.pop("interests")
        for interest in interests:
            current_interest = Interest.objects.get(**interest)
            UserInterest.objects.create(
                user=instance, interest=current_interest
            )
        return super().update(instance, validated_data)


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

    interests = InterestSerializer(many=True)

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
            "event_price",
            "image",
        )

    def create(self, validated_data):
        """Создание мероприятия с указанными интересами."""
        if "interests" not in self.initial_data:
            return Event.objects.create(**validated_data)
        interests = validated_data.pop("interests")
        event = Event.objects.create(**validated_data)
        for interest in interests:
            current_interest = Interest.objects.get(**interest)
            EventInterest.objects.create(
                event=event, interest=current_interest
            )
        return event

    def update(self, instance, validated_data):
        """Обновление мероприятия с указанными интересами."""
        if "interests" not in self.initial_data:
            return super().update(instance, validated_data)
        interests = validated_data.pop("interests")
        for interest in interests:
            current_interest = Interest.objects.get(**interest)
            EventInterest.objects.create(
                event=instance, interest=current_interest
            )
        return super().update(instance, validated_data)
