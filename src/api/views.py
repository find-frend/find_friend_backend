from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from events.models import Event
from users.models import Friend, User

from .filters import EventSearchFilter, EventsFilter, UserFilter
from .pagination import EventPagination, MyPagination
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (
    EventSerializer,
    FriendSerializer,
    MyUserGetSerializer,
    MyUserSerializer,
)


class MyUserViewSet(UserViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = UserFilter
    search_fields = ["email", "first_name", "last_name"]
    permission_classes = [
        IsAdminOrAuthorOrReadOnly,
    ]

    def get_serializer_class(self):
        """Выбор сериализатора."""
        if self.request.method == "GET":
            return MyUserGetSerializer
        return MyUserSerializer


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
    permission_classes = [
        IsAdminOrAuthorOrReadOnly,
    ]
