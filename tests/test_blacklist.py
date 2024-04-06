from http import HTTPStatus

import pytest

from users.models import Blacklist


@pytest.mark.django_db(transaction=True)
class TestBlacklistAPI:
    """Тесты черного списка."""

    objects_url = "/api/v1/users/blacklist/"

    def check_blacklist_info(self, info, another_user, url):
        """Проверка содержания полей в черном списке."""
        fields = ["id", "email", "first_name", "last_name"]
        for field in fields:
            assert field in info, (
                f"Ответ на GET-запрос к `{url}` содержит "
                f"неполную информацию о черном списке. Проверьте, что поле "
                f"`{field}` добавлено в список полей `fields`"
                f"сериализатора модели `Blacklist`."
            )
        assert info["email"] == another_user.email, (
            f"Ответ на GET-запрос к `{url}` содержит "
            f"некорректную информацию о черном списке. Проверьте, что "
            f"в списке есть пользователь с email:`{another_user.email}`"
        )

    def test_blacklist_list_not_auth(self, client):
        """Проверка получения данных неавторизованного пользователя."""
        response = client.get(self.objects_url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            f"`{self.objects_url}` возвращает ответ со статусом 401."
        )

    def test_blacklist_list_auth(
        self, user_client, user, another_user, list_1, list_2
    ):
        """Проверка данных авторизованного пользователя."""
        response = user_client.get(self.objects_url)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f"Эндпоинт `{self.objects_url}` не найден, проверьте настройки"
            " в *urls.py*."
        )
        test_data = response.json()
        if "results" in test_data.keys():
            assert (
                len(test_data["results"])
                == Blacklist.objects.filter(user=user).count()
            ), (
                "Проверьте, что для авторизованного пользователя GET-запрос к "
                f"`{self.objects_url}` возвращает информацию обо всех "
                "существующих "
                "черных списках пользователя."
            )
            test_obj = test_data["results"][0]
            self.check_blacklist_info(test_obj, another_user, self.objects_url)
        else:
            assert (
                response.status_code == HTTPStatus.UNAUTHORIZED
            ), f"Ошибка доступа `{test_data['detail']}`"

    def test_blacklist_create_not_auth(self, client, user):
        """Проверка создания списка неавторизованного пользователя."""
        url = f"/api/v1/users/{user.id}/block/"
        data = {}
        response = client.post(url, data=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что неавторизованному пользователю при попытке "
            "создать список возвращается статус 401."
        )

    def test_blacklist_delete_not_auth(self, client, user):
        """Проверка удаления списка неавторизованного пользователя."""
        url = f"/api/v1/users/{user.id}/block/"
        response = client.delete(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что неавторизованному пользователю при попытке "
            "удалить список возвращается статус 401."
        )

    def test_blacklist_create_auth(self, user_client, another_user):
        """Проверка создания списка авторизованного пользователя."""
        url = f"/api/v1/users/{another_user.id}/block/"
        data = {}
        response = user_client.post(url, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            "Проверьте, что авторизованному пользователю при попытке "
            "создать список возвращается статус 201."
        )

    def test_blacklist_delete_auth(self, user_client, another_user, list_1):
        """Проверка удаления списка авторизованного пользователя."""
        url = f"/api/v1/users/{another_user.id}/block/"
        response = user_client.delete(url)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            "Проверьте, что авторизованному пользователю при попытке "
            "удалить список возвращается статус 204."
        )
