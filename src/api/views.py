from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from events.models import Event
from users.models import Friend, User

from .filters import EventSearchFilter, EventsFilter, UserFilter
from .pagination import EventPagination, MyPagination
from .serializers import EventSerializer, FriendSerializer, MyUserSerializer


class MyUserViewSet(UserViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = UserFilter
    search_fields = ["first_name", "last_name"]


class FriendViewSet(ModelViewSet):
    """Вьюсет друга пользователя."""

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    pagination_class = MyPagination


class EventViewSet(ModelViewSet):
    """Вьюсет мероприятия пользователя."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (EventSearchFilter, DjangoFilterBackend)
    filterset_class = EventsFilter
    pagination_class = EventPagination
