from djoser.views import UserViewSet

from users.models import User

from .pagination import MyPagination
from .serializers import MyUserSerializer


class MyUserViewSet(UserViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyPagination
