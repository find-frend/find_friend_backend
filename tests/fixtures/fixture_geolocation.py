import pytest

from events.models import Event, EventLocation
from users.models import City, UserLocation


@pytest.fixture
def city1():
    """Тестовые данные для города 1."""
    return City.objects.create(name="Москва")


@pytest.fixture
def city2():
    """Тестовые данные для города 2."""
    return City.objects.create(name="Тула")


@pytest.fixture
def event_g1(city1):
    """Тестовые данные для мероприятия 1."""
    return Event.objects.create(
        name="Название 1",
        description="description_1",
        event_type="event_type_1",
        event_price=100,
        city=city1,
        address="Кремль",
        min_age=10,
        max_age=20,
        min_count_members=5,
        max_count_members=10,
    )


@pytest.fixture
def event_g2(city2):
    """Тестовые данные для мероприятия 1."""
    return Event.objects.create(
        name="Название 2",
        description="description_2",
        event_type="event_type_2",
        event_price=200,
        city=city2,
        address="пл. Ленина, 1",
        min_age=20,
        max_age=30,
        min_count_members=5,
        max_count_members=10,
    )


@pytest.fixture
def user_location_1(user):
    """Тестовые данные 1."""
    return UserLocation.objects.create(user=user, lon=37.606800, lat=55.738600)


@pytest.fixture
def user_location_2(another_user):
    """Тестовые данные 2."""
    return UserLocation.objects.create(
        user=another_user, lon=31.617900, lat=54.202100
    )


@pytest.fixture
def event_location_1(event_g1):
    """Тестовые данные 1."""
    return EventLocation.objects.create(
        event=event_g1, lon=37.606800, lat=55.738600
    )


@pytest.fixture
def event_location_2(event_g2):
    """Тестовые данные 2."""
    return EventLocation.objects.create(
        event=event_g2, lon=31.617900, lat=54.202100
    )
