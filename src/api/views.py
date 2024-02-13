from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet

from users.models import Profile, User

from .pagination import MyPagination
from .serializers import MyUserSerializer, ProfileSerializer


class MyUserViewSet(UserViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyPagination


class ProfileViewSet(ModelViewSet):
    """Вьюсет профиля пользователя."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
