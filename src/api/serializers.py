from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers  # , status
# from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from config import settings
from events.models import Event, EventMember
from users.models import City, FriendRequest, Interest, User  # UserInterest
from users.validators import (EMAIL_LENGTH_MSG, FIRST_NAME_LENGTH_MSG,
                              INVALID_EMAIL_MSG, LAST_NAME_LENGTH_MSG)


class InterestSerializer(ModelSerializer):
    """Сериализатор интересов."""

    class Meta:
        model = Interest
        fields = ("id", "name")


class MyUserBaseSerializer(serializers.Serializer):
    """Базовый сериализатор пользователя."""

    class Meta:
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "max_length": EMAIL_LENGTH_MSG,
                    "min_length": EMAIL_LENGTH_MSG,
                    "invalid": INVALID_EMAIL_MSG,
                }
            },
            "first_name": {
                "error_messages": {
                    "max_length": FIRST_NAME_LENGTH_MSG,
                    "min_length": FIRST_NAME_LENGTH_MSG,
                }
            },
            "last_name": {
                "error_messages": {
                    "max_length": LAST_NAME_LENGTH_MSG,
                    "min_length": LAST_NAME_LENGTH_MSG,
                }
            },
        }


class GetFriendsField(serializers.RelatedField):
    """Сериализатор списка друзей."""

    def to_representation(self, value):
        """Представление списка друзей."""
        return {"id": value.pk}


class MyUserSerializer(UserSerializer, MyUserBaseSerializer):
    """Сериализатор пользователя."""

    city = SlugRelatedField(
        slug_field="name",
        queryset=City.objects.all(),
        required=False,
        allow_null=True,
    )
    first_name = serializers.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        min_length=settings.MIN_LENGTH_CHAR,
        allow_blank=False,
        required=False,
    )
    last_name = serializers.CharField(
        max_length=settings.MAX_LENGTH_CHAR,
        min_length=settings.MIN_LENGTH_CHAR,
        allow_blank=False,
        required=False,
    )
    interests = InterestSerializer(many=True, required=False)
    friends = GetFriendsField(read_only=True, many=True, required=False)
    age = serializers.IntegerField(required=False)
    friends_count = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
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
        )
        extra_kwargs = {**MyUserBaseSerializer.Meta.extra_kwargs}

    # def create(self, validated_data):
    #     """Создание пользователя с указанными интересами и друзьями."""
    #     is_interests = False
    #     is_friends = False
    #     if "interests" in self.initial_data:
    #         interests = validated_data.pop("interests")
    #         is_interests = True
    #     if "friends" in self.initial_data:
    #         friends = self.initial_data.pop("friends")
    #         is_friends = True
    #     user = User.objects.create(**validated_data)
    #     if is_interests:
    #         for interest in interests:
    #             current_interest = Interest.objects.get(**interest)
    #             UserInterest.objects.create(
    #                 user=user, interest=current_interest
    #             )
    #     if is_friends:
    #         is_addeds = []
    #         for friend in friends:
    #             friends_list = Friend.objects.filter(
    #                 initiator=user, friend=friend["id"]
    #             )
    #             if friends_list:
    #                 is_addeds.append(friends_list[0].is_added)
    #             else:
    #                 is_addeds.append(False)
    #         for i, friend in enumerate(friends):
    #             current_friend = User.objects.get(**friend)
    #             Friend.objects.create(
    #                 initiator=user,
    #                 friend=current_friend,
    #                 is_added=is_addeds[i],
    #             )
    #     return user
    #
    # def update(self, instance, validated_data):
    #     """Обновление пользователя с указанными интересами и друзьями."""
    #     if "interests" in self.initial_data:
    #         interests = validated_data.pop("interests")
    #         instance.interests.clear()
    #         for interest in interests:
    #             current_interest = Interest.objects.get(**interest)
    #             UserInterest.objects.create(
    #                 user=instance, interest=current_interest
    #             )
    #     if "friends" in self.initial_data:
    #         # friends = validated_data.pop("friends")
    #         friends = self.initial_data.pop("friends")
    #         is_addeds = []
    #         for friend in friends:
    #             friends_list = Friend.objects.filter(
    #                 initiator=instance, friend=friend["id"]
    #             )
    #             if friends_list:
    #                 is_addeds.append(friends_list[0].is_added)
    #             else:
    #                 is_addeds.append(False)
    #         instance.friends.clear()
    #         for i, friend in enumerate(friends):
    #             current_friend = User.objects.get(**friend)
    #             Friend.objects.create(
    #                 initiator=instance,
    #                 friend=current_friend,
    #                 is_added=is_addeds[i],
    #             )
    #     return super().update(instance, validated_data)


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

    # class FriendSerializer(ModelSerializer):
    #     """Сериализатор друга пользователя."""
    #
    #     initiator = MyUserSerializer(read_only=True)
    #     friend = MyUserSerializer(read_only=True)
    #
    #     class Meta:
    #         model = Friend
    #         fields = (
    #             "id",
    #             "initiator",
    #             "friend",
    #             "is_added",
    #         )

    '''
    def validate(self, data):
        """Валидация друзей."""
        if not data:
            raise ValidationError(
                detail="Ошибка с выбором друга",
                code=status.HTTP_400_BAD_REQUEST,
            )
        initiator = data.get("initiator")
        friend = data.get("friend")

        if not initiator or not initiator.is_active:
            raise ValidationError(
                detail=f"Нет такого пользователя {initiator}",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not friend or not friend.is_active:
            raise ValidationError(
                detail=f"Нет такого друга {friend}",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if initiator == friend:
            raise ValidationError(
                detail="Дружба с самим собой невозможна",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if (
            Friend.objects.filter(initiator=initiator, friend=friend).exists()
            or Friend.objects.filter(
                initiator=friend, friend=initiator).exists()
        ):
            raise ValidationError(
                detail="Повторная дружба невозможна",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
        '''


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели FriendRequest,
    обрабатывающий входные и выходные данные API заявок на дружбу.
    """

    class Meta:
        model = FriendRequest
        fields = "__all__"
        read_only_fields = ("from_user", "status")

    def validate(self, data):
        """
        Проверяет валидность данных перед созданием объекта заявки на дружбу.
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
    """Сериализатор мероприятия пользователя."""

    # interests = InterestSerializer(many=True)
    members = GetMembersField(read_only=True, many=True, required=False)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            # "interests",
            "members",
            "event_type",
            "date",
            "city",
            "event_price",
            "image",
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
            return Event.objects.create(**validated_data)
        # members = validated_data.pop("members")
        members = self.initial_data.pop("members")
        event = Event.objects.create(**validated_data)
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


class CitySerializer(ModelSerializer):
    """Сериализатор городов."""

    class Meta:
        model = City
        fields = ("id", "name")
