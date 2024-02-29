from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from events.models import Event
from users.models import Friend, User

from .filters import EventSearchFilter, EventsFilter, UserFilter
from .pagination import EventPagination, MyPagination
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (EventSerializer, FriendSerializer,
                          MyUserGetSerializer, MyUserSerializer)
from .services import FriendRequestService


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


class FriendRequestViewSet(ModelViewSet):
    """Вьюсет добавления в друзья."""
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return FriendRequestService.get_user_friend_requests(self.request.user)

    def perform_create(self, serializer):
        friend_id = self.request.data.get('friend')
        if friend_id is not None:
            serializer.save(initiator=self.request.user, friend_id=friend_id)
        else:
            raise ValueError("ID друга не был передан")

    # def perform_create(self, serializer):
    #     FriendRequestService.create_friend_request(serializer,
    #                                                self.request.user)

    @action(detail=True, methods=['post'], url_path='accept')
    def accept_request(self, request, pk=None):
        message = FriendRequestService.respond_to_friend_request(pk,
                                                                 request.user,
                                                                 True)
        return Response({"message": message}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='decline')
    def decline_request(self, request, pk=None):
        message = FriendRequestService.respond_to_friend_request(pk,
                                                                 request.user,
                                                                 False)
        return Response({"message": message}, status=status.HTTP_200_OK)


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
