from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet

from events.models import Event
from users.models import Friend, User

from .pagination import MyPagination, EventPagination
from .serializers import EventSerializer, FriendSerializer, MyUserSerializer


class MyUserViewSet(UserViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyPagination


class FriendViewSet(ModelViewSet):
    """Вьюсет друга пользователя."""

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    pagination_class = MyPagination


class EventViewSet(ModelViewSet):
    """Вьюсет мероприятия пользователя."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventPagination
