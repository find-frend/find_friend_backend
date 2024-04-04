import pytest

from users.models import Blacklist


@pytest.fixture
def list_1(user, another_user):
    """Тестовые данные 1."""
    return Blacklist.objects.create(user=user, blocked_user=another_user)


@pytest.fixture
def list_2(user, another_user):
    """Тестовые данные 2."""
    return Blacklist.objects.create(user=another_user, blocked_user=user)
