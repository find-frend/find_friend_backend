from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet

from events.models import Event
from notifications.models import Notification
from users.models import Friend, Profile, User

from .pagination import MyPagination
from .serializers import (
    EventSerializer,
    FriendSerializer,
    MyUserSerializer,
    NotificationSerializer,
    ProfileSerializer,
)


class MyUserViewSet(UserViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyPagination


class ProfileViewSet(ModelViewSet):
    """Вьюсет профиля пользователя."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class FriendViewSet(ModelViewSet):
    """Вьюсет друга пользователя."""

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer


class EventViewSet(ModelViewSet):
    """Вьюсет мероприятия пользователя."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class NotificationViewSet(ModelViewSet):
    """Вьюсет уведомлений."""

    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)
