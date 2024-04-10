from http import HTTPStatus
from time import sleep

import pytest

from events.models import EventLocation

API_URL = "/api/v1"


@pytest.mark.django_db(transaction=True)
class TestEventGeolocatioAPI:
    """Тесты черного списка."""

    def test_event_save_location_auth(self, user_client, user, event_g2):
        """Проверка сохранения геолокации мероприятия от авторизованного.

        пользователя.
        """
        url = f"{API_URL}/events/{event_g2.id}/"
        data = {
            "address": "проспект Ленина, 16",
        }
        for retry in range(10):
            response = user_client.patch(url, data=data)
            if response.status_code != 403:
                break
            sleep(5)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "сохранить геолокацию мероприятия возвращается статус 200."
        )
        location = EventLocation.objects.filter(event=event_g2)
        assert len(location) == 1, (
            "Проверьте, что авторизованному пользователю при попытке "
            "сохранить геолокацию мероприятия геолокация создается."
        )
        assert location[0].event == event_g2, (
            f"Проверьте, что " f"сохранена геолокация мероприятия:`{event_g2}`"
        )
