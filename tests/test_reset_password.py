from http import HTTPStatus

import pytest
from django.core import mail


@pytest.mark.django_db(transaction=True)
class TestPasswordReset:
    """Тесты для смены пароля."""

    register_url = "/api/v1/users/"
    login_url = "/api/v1/auth/token/login/"
    send_reset_password_email_url = "/api/v1/users/reset_password/"
    confirm_reset_password_url = "/api/v1/users/reset_password/confirm/"

    user_data = {
        "email": "test@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "verysecret",
    }
    login_data = {"email": "test@example.com", "password": "verysecret"}

    def test_reset_password(self, client):
        """Проверка смены пароля пользователя."""
        # регистрация пользователя
        response = client.post(self.register_url, self.user_data)
        assert (
            response.status_code == HTTPStatus.CREATED
        ), f"Страница `{self.register_url}` работает неправильно!"

        # запрос на смену пароля
        data = {"email": self.user_data["email"]}
        response = client.post(self.send_reset_password_email_url, data)
        assert response.status_code == HTTPStatus.OK, (
            f"Страница {self.send_reset_password_email_url} "
            f"работает неправильно!"
        )
        # получение токена для сброса пароля
        email_lines = mail.outbox[0].body.splitlines()
        token_line = [
            i for i in email_lines if "Ваш код для восстановления пароля:" in i
        ][0]
        token = token_line.split(" ")[-1:]

        # подтверждение смены пароля
        data = {"token": token, "password": "new_verysecret"}
        response = client.post(self.confirm_reset_password_url, data)
        assert response.status_code == HTTPStatus.OK, (
            f"Страница {self.confirm_reset_password_url} "
            f"работает неправильно!"
        )

        # вход со старым паролем
        response = client.post(self.login_url, self.login_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"При входе со старым паролем"
            f"должен возвращаться статус {HTTPStatus.BAD_REQUEST}, "
            f"а был возвращен {response.status_code}."
        )

        # вход с новым паролем
        login_data = dict(self.login_data)
        login_data["password"] = "new_verysecret"
        response = client.post(self.login_url, login_data)
        assert response.status_code == HTTPStatus.OK, (
            f"При входе с новым паролем"
            f"должен возвращаться статус {HTTPStatus.OK}, "
            f"а был возвращен {response.status_code}."
        )

    def test_reset_password_wrong_email(self, client):
        """Проверка смены пароля при указании некорректной почты."""
        data = {"email": "wrong@email.com"}
        response = client.post(self.send_reset_password_email_url, data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"Адрес электронной почты {data['email']} не соответствует тому, "
            f"что указан при регистрации."
        )
        assert len(mail.outbox) == 0, (
            f"Письмо с кодом для смены пароля не должно отправляться на адрес"
            f"{data['email']}, отличный от того, что указан при регистрации."
        )
