import pytest


@pytest.fixture
def user(django_user_model):
    """Тестовые данные для пользователя 1."""
    return django_user_model.objects.create_user(
        first_name="TestUser1",
        last_name="TestUser",
        password="1234567",
        email="test@tesr.ru",
    )


@pytest.fixture
def user_2(django_user_model):
    """Тестовые данные для пользователя 2."""
    return django_user_model.objects.create_user(
        first_name="TestUser2",
        last_name="TestUser",
        password="1234567",
        email="test@tesr.ru",
    )
