from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from events.models import Event
from users.models import Friend, User

from .pagination import MyPagination
from .serializers import EventSerializer, FriendSerializer, MyUserSerializer
from .filters import UserFilter, UserSearchFilter


class MyUserViewSet(UserViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyPagination
    filter_backends = (UserSearchFilter, DjangoFilterBackend)
    filterset_class = UserFilter


class FriendViewSet(ModelViewSet):
    """Вьюсет друга пользователя."""

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer


class EventViewSet(ModelViewSet):
    """Вьюсет мероприятия пользователя."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
