# from http import HTTPStatus
# from django.db.utils import IntegrityError
import pytest

# from events.models import Event


@pytest.mark.django_db(transaction=True)
class TestEventsAPI:
    """Тесты по мероприятиям."""

    def test_check_data(self):
        """Проверка мероприятия 1."""
        assert 1 == 1

    def test_check_data2(self):
        """Проверка мероприятия 2."""
        assert 5 == 4
