from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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

    @swagger_auto_schema(
        responses={
            400: openapi.Response(
                description='Bad Request',
                examples={
                    'application/json': {
                            'first_name': ['Обязательное поле.'],
                            'last_name': ['Обязательное поле.'],
                            'age': ['Обязательное поле.'],
                            'interests': ['Обязательное поле.'],
                            'friends_count': ['Обязательное поле.']
                    }
                }
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            401: openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail': 'Учетные данные не были предоставлены.'
                    }
                }
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FriendViewSet(ModelViewSet):
    """Вьюсет друга пользователя."""

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        responses={
            401: openapi.Response(
                description='UnauthorizedAccess',
                examples={
                    'application/json': {
                        'detail': 'Учетные данные не были предоставлены.'
                    }
                }
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            401: openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail': 'Учетные данные не были предоставлены.'
                    }
                }
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


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

    @swagger_auto_schema(
        responses={
            401: openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail': 'Учетные данные не были предоставлены.'
                    }
                }
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            401: openapi.Response(
                description='Unauthorized',
                examples={
                    'application/json': {
                        'detail': 'Учетные данные не были предоставлены.'
                    }
                }
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
