import pytest

from events.models import Event
from users.models import City


@pytest.fixture
def city():
    """Тестовые данные для города 1."""
    return City.objects.create(name="Москва")


@pytest.fixture
def event_1(city):
    """Тестовые данные для мероприятия 1."""
    return Event.objects.create(
        name="Название 1",
        description="description_1",
        event_type="event_type_1",
        event_price=100,
        city=city,
        min_age=10,
        max_age=20,
        min_count_members=5,
        max_count_members=10,
    )


@pytest.fixture
def event_2(city):
    """Тестовые данные для мероприятия 1."""
    return Event.objects.create(
        name="Название 2",
        description="description_2",
        event_type="event_type_2",
        event_price=200,
        city=city,
        min_age=20,
        max_age=30,
        min_count_members=5,
        max_count_members=10,
    )
