from http import HTTPStatus

import pytest

from events.models import Event

# from django.db.utils import IntegrityError


@pytest.mark.django_db(transaction=True)
class TestEventsAPI:
    """Тесты по мероприятиям."""

    event_url = "/api/v1/events/"
    event_detail_url = "/api/v1/events/{event_id}/"

    def check_event_info(self, event_info, url):
        """Проверка содержания полей в мероприятии."""
        assert (
            "id" in event_info
        ), f"""Ответ на GET-запрос к `{url}`
            содержит неполную информацию о мероприятии. Проверьте, что поле
            `id` добавлено в список полей `fields` сериализатора модели
            `Event`."""
        assert (
            "name" in event_info
        ), f"""Ответ на GET-запрос к `{url}`
            содержит неполную информацию о мероприятии. Проверьте, что поле
            `name` добавлено в список полей `fields` сериализатора модели
            `Event`."""
        assert (
            "description" in event_info
        ), f"""Ответ на GET-запрос к `{url}`
            содержит неполную информацию о мероприятии. Проверьте, что поле
            `name` добавлено в список полей `fields` сериализатора модели
            `Event`."""

    def test_event_not_found(self, client, event_1, event_2):
        """Проверка мероприятия 1."""
        response = client.get(self.event_url)
        test_data = response.json()
        assert len(test_data["results"]) == Event.objects.count(), (
            "Проверьте, что для авторизованного пользователя GET-запрос к "
            f"`{self.event_url}` возвращает информацию обо всех существующих "
            "мероприятиях."
        )
        test_event = test_data["results"][0]
        self.check_event_info(test_event, self.event_url)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f"Эндпоинт `{self.event_url}` не найден, проверьте настройки в "
            "*urls.py*."
        )

    def test_event_list_not_auth(self, client, event_1):
        """Проверка получения данных неавторизованного пользователя."""
        response = client.get(self.event_url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            f"`{self.event_url}` возвращает ответ со статусом 200."
        )

    def test_event_create(self, client, event_1):
        """Проверка создания мероприятия неавторизованного пользователя."""
        data = {"name": "Название номер 3", "description": "description_3"}
        response = client.post(self.event_url, data=data)
        assert (
            response.status_code == HTTPStatus.UNAUTHORIZED
        ), """Проверьте, что неавторизованному пользователю при попытке
            создать мероприятие возвращается статус 401."""
