from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email as django_validate_email
from django.db.models import Q
from djoser.serializers import (
    TokenCreateSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from config import constants
from config.constants import messages
from events.models import Event, EventMember
from notifications.models import Notification, NotificationSettings
from users.models import (
    Blacklist,
    City,
    FriendRequest,
    Friendship,
    Interest,
    User,
    UserInterest,
)
from users.validators import validate_email, validate_password

from .geo import save_event_location


class CustomTokenCreateSerializer(TokenCreateSerializer):
    """Кастомный сериализатор создания токена при аутентификации."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        """Валидация данных при аутентификации."""
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        validate_email(email)
        try:
            django_validate_email(email)
        except DjangoValidationError:
            raise ValidationError(messages.INVALID_EMAIL_MSG)
        validate_password(password)

        params = {"email": email}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")

        if self.user and self.user.is_active:
            return attrs

        self.fail("invalid_credentials")
        return None


class InterestSerializer(ModelSerializer):
    """Сериализатор интересов."""

    class Meta:
        model = Interest
        fields = ("id", "name")


class GetFriendsField(serializers.RelatedField):
    """Сериализатор списка друзей."""

    def to_representation(self, value):
        """Представление списка друзей."""
        return {
            "id": value.pk,
            "first_name": value.first_name,
            "last_name": value.last_name,
            "age": value.age(),
            # "city": value.city.name,
        }


class MyUserBaseSerializer(serializers.Serializer):
    """Базовый сериализатор пользователя."""

    class Meta:
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "max_length": messages.EMAIL_LENGTH_MSG,
                    "min_length": messages.EMAIL_LENGTH_MSG,
                    "invalid": messages.INVALID_EMAIL_MSG,
                }
            },
            "first_name": {
                "error_messages": {
                    "max_length": messages.FIRST_NAME_LENGTH_MSG,
                    "min_length": messages.FIRST_NAME_LENGTH_MSG,
                }
            },
            "last_name": {
                "error_messages": {
                    "max_length": messages.LAST_NAME_LENGTH_MSG,
                    "min_length": messages.LAST_NAME_LENGTH_MSG,
                }
            },
        }


class MyUserSerializer(UserSerializer, MyUserBaseSerializer):
    """Сериализатор пользователя."""

    is_blocked = SerializerMethodField(read_only=True)

    city = SlugRelatedField(
        slug_field="name",
        queryset=City.objects.all(),
        required=False,
        allow_null=True,
    )
    interests = InterestSerializer(many=True, required=False)
    friends = GetFriendsField(read_only=True, many=True, required=False)
    age = serializers.IntegerField(required=False)
    friends_count = serializers.IntegerField(required=False)
    network_nick = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "birthday",
            "sex",
            "age",
            "interests",
            "friends",
            "friends_count",
            "city",
            "interests",
            "avatar",
            "profession",
            "purpose",
            "network_nick",
            "additionally",
            "is_geoip_allowed",
            "is_blocked",
        )

        extra_kwargs = {**MyUserBaseSerializer.Meta.extra_kwargs}

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
        """Обновление пользователя с указанными интересами и друзьями.

        Друзей можно только удалять.
        """
        if "interests" in self.initial_data:
            interests = validated_data.pop("interests")
            instance.interests.clear()
            for interest in interests:
                current_interest = Interest.objects.get(**interest)
                UserInterest.objects.create(
                    user=instance, interest=current_interest
                )
        current_friends = instance.friends
        if current_friends.exists() and "friends" in self.initial_data:
            friends = self.initial_data.pop("friends")
            friends_list = []
            for friend in friends:
                friends_list.append(friend["id"])
            new_friends = []
            current_friends = current_friends.values()
            for current_friend in current_friends:
                if current_friend["id"] in friends_list:
                    new_friends.append(current_friend["id"])
            instance.friends.clear()
            instance.friends.set(new_friends)
        return super().update(instance, validated_data)

    def get_network_nick(self, obj):
        """Метод сериализатора для ограничения просмотра поля network_nick."""
        request = self.context.get("request")

        if (
            Friendship.objects.filter(
                # Q(is_added=True),
                Q(initiator=request.user, friend=obj)
                | Q(initiator=obj, friend=request.user),
            ).exists()
        ) or obj == request.user:
            return obj.network_nick
        return None

    def get_is_blocked(self, blocked_user):
        """Метод сериализатора для просмотра блокировки пользователя."""
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Blacklist.objects.filter(
            user=user, blocked_user=blocked_user
        ).exists()


class MyUserCreateSerializer(UserCreateSerializer, MyUserBaseSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            "password",
            "birthday",
        )
        extra_kwargs = {**MyUserBaseSerializer.Meta.extra_kwargs}


class MyUserGetSerializer(UserSerializer):
    """Сериализатор пользователя."""

    city = SlugRelatedField(
        slug_field="name",
        queryset=City.objects.all(),
        required=False,
        allow_null=True,
    )
    age = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "age",
            "city",
        )


class FriendRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для модели FriendRequest.

    обрабатывает входные и выходные данные API заявок на дружбу.
    """

    class Meta:
        model = FriendRequest
        fields = "__all__"
        read_only_fields = ("from_user", "status")

    def validate(self, data):
        """Проверяет валидность данных.

        Перед созданием объекта заявки на дружбу.
        """
        if data["to_user"] == self.context["request"].user:
            raise serializers.ValidationError(
                "Вы не можете отправить заявку на дружбу самому себе."
            )
        if FriendRequest.objects.filter(
            from_user=self.context["request"].user, to_user=data["to_user"]
        ).exists():
            raise serializers.ValidationError(
                "Заявка на дружбу этому пользователю уже отправлена."
            )
        return data


class GetMembersField(serializers.RelatedField):
    """Сериализатор списка участников мероприятия."""

    def to_representation(self, value):
        """Представление списка участников мероприятия."""
        return {"id": value.pk}


class EventSerializer(ModelSerializer):
    """Сериализатор мероприятия."""

    # interests = InterestSerializer(many=True)
    members = GetMembersField(read_only=True, many=True, required=False)
    members_count = serializers.IntegerField(required=False)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            # "interests",
            "members",
            "event_type",
            "start_date",
            "end_date",
            "city",
            "address",
            "event_price",
            "image",
            "members_count",
            "min_age",
            "max_age",
            "min_count_members",
            "max_count_members",
        )

    '''
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
    '''

    def create(self, validated_data):
        """Создание мероприятия с указанными участниками."""
        if "members" not in self.initial_data:
            event = Event.objects.create(**validated_data)
            if "city" in self.initial_data or "address" in self.initial_data:
                save_event_location(event, validated_data)
            return event
        # members = validated_data.pop("members")
        members = self.initial_data.pop("members")
        event = Event.objects.create(**validated_data)
        if "city" in self.initial_data or "address" in self.initial_data:
            save_event_location(event, validated_data)
        is_organizers = []
        for member in members:
            members_list = EventMember.objects.filter(
                event=event, user=member["id"]
            )
            if members_list:
                is_organizers.append(members_list[0].is_organizer)
            else:
                is_organizers.append(False)
        for i, member in enumerate(members):
            current_member = User.objects.get(**member)
            EventMember.objects.create(
                event=event, user=current_member, is_organizer=is_organizers[i]
            )
        return event

    def update(self, instance, validated_data):
        """Обновление мероприятия с указанными участниками."""
        if "city" in self.initial_data or "address" in self.initial_data:
            save_event_location(instance, validated_data)
        if "members" not in self.initial_data:
            return super().update(instance, validated_data)
        # members = validated_data.pop("members")
        members = self.initial_data.pop("members")
        is_organizers = []
        for member in members:
            members_list = EventMember.objects.filter(
                event=instance, user=member["id"]
            )
            if members_list:
                is_organizers.append(members_list[0].is_organizer)
            else:
                is_organizers.append(False)
        instance.members.clear()
        for i, member in enumerate(members):
            current_member = User.objects.get(**member)
            EventMember.objects.create(
                event=instance,
                user=current_member,
                is_organizer=is_organizers[i],
            )
        return super().update(instance, validated_data)


class MyEventSerializer(ModelSerializer):
    """Сериализатор списка мероприятий пользователя."""

    class Meta:
        model = Event
        fields = ("id", "name")


class CitySerializer(ModelSerializer):
    """Сериализатор городов."""

    class Meta:
        model = City
        fields = ("id", "name")


class BlacklistSerializer(MyUserSerializer):
    """Сериализатор черного списка."""

    class Meta(MyUserSerializer.Meta):
        fields = MyUserSerializer.Meta.fields
        read_only_fields = ("email", "first_name", "last_name")

    def validate(self, data):
        """Валидация черного списка."""
        blocked_user = self.instance
        user = self.context.get("request").user
        if Blacklist.objects.filter(
            blocked_user=blocked_user, user=user
        ).exists():
            raise ValidationError(
                detail="Повторная блокировка пользователя невозможна",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == blocked_user:
            raise ValidationError(
                detail="Блокировка себя невозможна",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class NotificationSerializer(ModelSerializer):

    """Сериализатор уведомлений."""

    class Meta:
        model = Notification
        fields = "__all__"


class NotificationSettingsSerializer(ModelSerializer):
    """Сериализатор найстройки уведомлений."""
    class Meta:
        model = NotificationSettings
        fields = '__all__'
