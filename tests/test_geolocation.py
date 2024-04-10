from http import HTTPStatus

import pytest

from users.models import UserLocation

API_URL = "/api/v1"


@pytest.mark.django_db(transaction=True)
class TestEventGeolocatioAPI:
    """Тесты черного списка."""

    def test_event_save_location_not_auth(
        self, client, another_user, event_g2
    ):
        """Проверка сохранения геолокации мероприятия от неавторизованного.

        пользователя.
        """
        url = f"{API_URL}/events/{event_g2.id}/"
        data = {"address": "проспект Ленина, 16"}
        response = client.patch(url, data=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что неавторизованному пользователю при попытке "
            "сохранить расстояние мероприятия возвращается статус 401."
        )

    def test_event_get_location_not_auth(
        self, client, event_g2, event_location_2
    ):
        """Проверка получения геолокации мероприятия неавторизованного.

        пользователя.
        """
        url = f"{API_URL}/events/{event_g2.id}/geolocation/"
        response = client.get(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что неавторизованному пользователю при попытке "
            "получить геолокацию мероприятия возвращается статус 401."
        )

    def test_event_get_location_auth(
        self, user_client, event_g1, event_location_1
    ):
        """Проверка получения геолокации мероприятия авторизованного.

        пользователя.
        """
        url = f"{API_URL}/events/{event_g1.id}/geolocation/"
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения геолокации мероприятия возвращается статус 200."
        )
        fields = ["latitude", "longitude"]
        info = response.json()
        for field in fields:
            assert field in info, (
                f"Ответ на GET-запрос к `{url}` содержит "
                f"неполную информацию о геолокации. Проверьте, что поле "
                f"`{field}` получено из модели `EventLocation`."
            )

    def test_event_get_distance_not_auth(
        self, client, another_user, user_location_2, event_g1, event_location_1
    ):
        """Проверка получения расстояния мероприятия от неавторизованного.

        пользователя.
        """
        url = f"{API_URL}/events/{event_g1.id}/distance/"
        response = client.get(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что неавторизованному пользователю при попытке "
            "получить расстояние до мероприятия возвращается статус 401."
        )

    def test_event_get_distance_auth(
        self, user_client, user, user_location_1, event_g2, event_location_2
    ):
        """Проверка получения расстояния пользователя с разрешением."""
        url = f"{API_URL}/events/{event_g2.id}/distance/"
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояния до мероприятия разрешением возвращается"
            " статус 200."
        )
        fields = ["distance"]
        info = response.json()
        for field in fields:
            assert field in info, (
                f"Ответ на GET-запрос к `{url}` содержит "
                f"неполную информацию о рассстоянии. Проверьте, что поле "
                f"`{field}` получено из модели `EventLocation`."
            )

    def test_event_get_distances_not_auth(
        self, client, another_user, user_location_2, event_g1, event_location_1
    ):
        """Проверка получения расстояний неавторизованного пользователя."""
        url = f"{API_URL}/events/distances/"
        response = client.get(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что неавторизованному пользователю при попытке "
            "получить расстояния возвращается статус 401."
        )

    def test_user_get_distances_auth(
        self,
        user_client,
        user,
        user_location_1,
        event_g1,
        event_location_1,
        event_g2,
        event_location_2,
    ):
        """Проверка получения расстояний до мероприятий."""
        url = f"{API_URL}/events/distances/"
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояний до мероприятий возвращается статус 200."
        )
        info = response.json()
        assert len(info) == 2, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояний до мероприятий возвращается 2 расстояния."
        )
        fields = ["event", "name", "distance"]
        for field in fields:
            assert field in info[0], (
                f"Ответ на GET-запрос к `{url}` содержит "
                f"неполную информацию о рассстоянии. Проверьте, что поле "
                f"`{field}` получено из модели `UserLocation`."
            )

    def test_user_get_distances_maxdistance(
        self,
        user_client,
        user,
        user_location_1,
        event_g1,
        event_location_1,
        event_g2,
        event_location_2,
    ):
        """Проверка получения расстояний до мероприятий c ограничением."""
        url = f"{API_URL}/events/distances/?search=100"
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояний до мероприятий возвращается статус 200."
        )
        info = response.json()
        assert len(info) == 1, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояний до мероприятий возвращается 1 расстояние."
        )


@pytest.mark.django_db(transaction=True)
class TestUserGeolocatioAPI:
    """Тесты черного списка."""

    def test_user_save_location_not_allowed(self, user_client, user):
        """Проверка сохранения геолокации пользователя без разрешения."""
        url = f"{API_URL}/users/{user.id}/"
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "сохранить геолокацию возвращается статус 200."
        )
        location = UserLocation.objects.filter(user=user)
        assert len(location) == 0, (
            "Проверьте, что авторизованному пользователю при попытке "
            "сохранить геолокацию без разрешения геолокация не создается."
        )

    def test_user_save_location_allowed(self, user_client, user):
        """Проверка сохранения геолокации пользователя с разрешением."""
        url = f"{API_URL}/users/{user.id}/"
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "сохранить геолокацию возвращается статус 200."
        )
        location = UserLocation.objects.filter(user=user)
        assert len(location) == 1, (
            "Проверьте, что авторизованному пользователю при попытке "
            "сохранить геолокацию c разрешением геолокация создается."
        )
        assert location[0].user == user, (
            f"Проверьте, что " f"сохранена геолокация пользователя:`{user}`"
        )

    def test_user_get_location_not_auth(
        self, client, another_user, user_location_2
    ):
        """Проверка получения геолокации неавторизованного пользователя."""
        url = f"{API_URL}/users/{another_user.id}/geolocation/"
        response = client.get(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что неавторизованному пользователю при попытке "
            "получить геолокацию возвращается статус 401."
        )

    def test_user_get_location_not_allowed(
        self, user_client, user, user_location_1
    ):
        """Проверка получения геолокации пользователя без разрешения."""
        url = f"{API_URL}/users/{user.id}/geolocation/"
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения геолокации без разрешения возвращается статус 404."
        )

    def test_user_get_location_allowed(
        self, user_client, user, user_location_1
    ):
        """Проверка получения геолокации пользователя с разрешением."""
        url = f"{API_URL}/users/{user.id}/geolocation/"
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения геолокации с разрешением возвращается статус 200."
        )
        fields = ["latitude", "longitude"]
        info = response.json()
        for field in fields:
            assert field in info, (
                f"Ответ на GET-запрос к `{url}` содержит "
                f"неполную информацию о геолокации. Проверьте, что поле "
                f"`{field}` получено из модели `UserLocation`."
            )

    def test_user_get_distance_not_auth(
        self, client, user, another_user, user_location_1, user_location_2
    ):
        """Проверка получения расстояния неавторизованного пользователя."""
        url = f"{API_URL}/users/{another_user.id}/distance/"
        response = client.get(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что неавторизованному пользователю при попытке "
            "получить расстояние возвращается статус 401."
        )

    def test_user_get_distance_not_allowed(
        self, user_client, user, another_user, user_location_1, user_location_2
    ):
        """Проверка получения расстояния пользователя без разрешения."""
        url = f"{API_URL}/users/{another_user.id}/distance/"
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояния без разрешения возвращается статус 404."
        )

    def test_user_get_distance_allowed(
        self, user_client, user, another_user, user_location_1, user_location_2
    ):
        """Проверка получения расстояния пользователя с разрешением."""
        url = f"{API_URL}/users/{another_user.id}/distance/"
        another_user.is_geoip_allowed = True
        another_user.save()
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояния с разрешением возвращается статус 200."
        )
        fields = ["distance"]
        info = response.json()
        for field in fields:
            assert field in info, (
                f"Ответ на GET-запрос к `{url}` содержит "
                f"неполную информацию о рассстоянии. Проверьте, что поле "
                f"`{field}` получено из модели `UserLocation`."
            )

    def test_user_get_distances_not_auth(
        self, client, user, another_user, user_location_1, user_location_2
    ):
        """Проверка получения расстояния неавторизованного пользователя."""
        url = f"{API_URL}/users/distances/"
        response = client.get(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что неавторизованному пользователю при попытке "
            "получить расстояние возвращается статус 401."
        )

    def test_user_get_distances_not_allowed(
        self, user_client, user, another_user, user_location_1, user_location_2
    ):
        """Проверка получения расстояния пользователя без разрешения."""
        url = f"{API_URL}/users/distances/"
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояния без разрешения возвращается статус 200."
        )
        info = response.json()
        assert len(info) == 0, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояния без разрешения возвращается пустой список."
        )

    def test_user_get_distances_allowed(
        self, user_client, user, another_user, user_location_1, user_location_2
    ):
        """Проверка получения расстояний до пользователей с разрешением."""
        url = f"{API_URL}/users/distances/"
        another_user.is_geoip_allowed = True
        another_user.save()
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояний с разрешением возвращается статус 200."
        )
        fields = ["user", "first_name", "last_name", "distance"]
        info = response.json()[0]
        for field in fields:
            assert field in info, (
                f"Ответ на GET-запрос к `{url}` содержит "
                f"неполную информацию о рассстоянии. Проверьте, что поле "
                f"`{field}` получено из модели `UserLocation`."
            )

    def test_user_get_distances_maxdistance(
        self, user_client, user, another_user, user_location_1, user_location_2
    ):
        """Проверка получения расстояний до пользователей c максимумом."""
        url = f"{API_URL}/users/distances/?search=100"
        another_user.is_geoip_allowed = True
        another_user.save()
        user.is_geoip_allowed = True
        user.save()
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояний с разрешением возвращается статус 200."
        )
        info = response.json()
        assert len(info) == 0, (
            "Проверьте, что авторизованному пользователю при попытке "
            "получения расстояния с ограничением возвращается пустой список."
        )
