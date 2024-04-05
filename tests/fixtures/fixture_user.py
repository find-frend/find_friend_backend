import pytest

from users.models import Friendship


@pytest.fixture
def user(django_user_model):
    """Тестовые данные для пользователя 1."""
    return django_user_model.objects.create_user(
        first_name="Тестовый",
        last_name="Юзер",
        password="alskdj01",
        email="testone@test.ru",
    )


@pytest.fixture
def another_user(django_user_model):
    """Тестовые данные для пользователя 2."""
    return django_user_model.objects.create_user(
        first_name="Второй",
        last_name="Юзер",
        password="alskdj02",
        email="testtwo@test.ru",
    )


@pytest.fixture
def third_user(django_user_model):
    """Тестовые данные для пользователя 3."""
    return django_user_model.objects.create_user(
        first_name="Третий",
        last_name="Юзер",
        password="alskdj03",
        email="testthree@test.ru",
    )


@pytest.fixture
def create_token():
    """Фабрика создания токена для пользователя."""

    def _create_token(_user):
        from rest_framework.authtoken.models import Token

        token, _ = Token.objects.get_or_create(user=_user)
        return token.key

    return _create_token


@pytest.fixture
def user_client(create_token, user):
    """Создание клиента для аутентифицированного пользователя."""
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {create_token(user)}")
    return client


@pytest.fixture
def friends(db, user, another_user):
    """Дружба между пользователями."""
    return Friendship.objects.create(initiator=user, friend=another_user)
