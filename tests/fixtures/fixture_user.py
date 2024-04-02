import pytest


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
def token(user):
    """Создание токена для пользователя."""
    from rest_framework.authtoken.models import Token

    token, _ = Token.objects.get_or_create(user=user)
    return token.key


@pytest.fixture
def user_client(token):
    """Создание клиента для аутентифицированного пользователя."""
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return client
