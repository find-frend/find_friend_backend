import random
import string
from http import HTTPStatus

import pytest

from config import constants as cnst
from config.constants import messages as msg


def generate_long_email(length):
    """Генерация слишком длинного адреса электронной почты."""
    local_part = "".join(
        random.choices(string.ascii_letters + string.digits, k=length - 15)
    )
    domain = "".join(random.choices(string.ascii_lowercase, k=250))
    return local_part + "@" + domain + ".com"


def generate_long_string(length):
    """Генерация слишком длинной строки."""
    return "".join(random.choices(string.ascii_letters, k=length))


@pytest.mark.django_db(transaction=True)
class TestAuthAPI:
    """Тесты аутентификации."""

    login_url = "/api/v1/auth/token/login/"
    logout_url = "/api/v1/auth/token/logout/"
    user_profile_url = "/api/v1/users/me/"

    def test_auth_correct_data(self, client, user):
        """Проверка успешного входа в систему при вводе корректных данных."""
        response = client.post(
            self.login_url,
            data={"email": user.email, "password": "alskdj01"},
        )

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f"Страница `{self.login_url}` не найдена, проверьте этот адрес "
            "в *urls.py*"
        )

        assert (
            response.status_code == HTTPStatus.OK
        ), f"Страница `{self.login_url}` работает неправильно!"

        auth_data = response.json()
        assert "auth_token" in auth_data, (
            f"Проверьте, что при POST запросе `{self.login_url}` "
            "возвращаете токен"
        )

    @pytest.mark.parametrize(
        "email,error_text",
        [
            ("русскиесимволы@test.ru", msg.EMAIL_ENGLISH_ONLY_MSG),
            ("invalidemail.ru", msg.INVALID_EMAIL_MSG),
            ("a@a", msg.EMAIL_LENGTH_MSG),
            (
                generate_long_email(cnst.MAX_LENGTH_EMAIL + 1),
                msg.EMAIL_LENGTH_MSG,
            ),
            ("wrong<>symbols@test.ru", msg.INVALID_EMAIL_MSG),
        ],
        ids=[
            "rus_symbols",
            "invalid_format",
            "too_short",
            "too_long",
            "wrong_symbols",
        ],
    )
    def test_auth_invalid_email(self, client, email, error_text):
        """Проверка ввода электронной почты в некорректном формате."""
        response = client.post(
            self.login_url,
            data={"email": email, "password": "rndmpsswd"},
        )
        assert error_text == response.json()["non_field_errors"][0], (
            f"При передаче {email} на `{self.login_url}` "
            f"должен возвращаться текст ошибки `{error_text}`, "
            f"а вернулся `{response.json()['non_field_errors'][0]}`."
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"При передаче {email} на `{self.login_url}` "
            f"должен возвращаться статус {HTTPStatus.BAD_REQUEST}, "
            f"а был возвращен {response.status_code}."
        )

    @pytest.mark.parametrize(
        "password,error_text",
        [
            ("short", msg.PASSWORD_LENGTH_MSG),
            (
                generate_long_string(cnst.MAX_LENGTH_PASSWORD + 1),
                msg.PASSWORD_LENGTH_MSG,
            ),
        ],
        ids=["too_short", "too_long"],
    )
    def test_auth_invalid_password(self, client, password, error_text):
        """Проверка ввода пароля в некорректном формате."""
        response = client.post(
            self.login_url,
            data={"email": "a@a.ru", "password": password},
        )
        assert error_text == response.json()["non_field_errors"][0], (
            f"При передаче {password} на `{self.login_url}` "
            f"должен возвращаться текст ошибки `{error_text}`, "
            f"а вернулся `{response.json()['non_field_errors'][0]}`."
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"При передаче {password} на `{self.login_url}` "
            f"должен возвращаться статус {HTTPStatus.BAD_REQUEST}, "
            f"а был возвращен {response.status_code}."
        )

    @pytest.mark.parametrize(
        "email,password",
        [(" ", "validpasswd"), ("validemail@test.ru", " ")],
        ids=["empty_email", "empty_password"],
    )
    def test_auth_empty_fields(self, client, email, password):
        """Проверка ввода пустых полей."""
        response = client.post(
            self.login_url,
            data={"email": email, "password": password},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"При передаче пустых полей на `{self.login_url}` "
            f"должен возвращаться статус {HTTPStatus.BAD_REQUEST}, а не "
            f"{response.status_code}."
        )
        assert [msg.FIELD_CANNOT_BE_BLANK_MSG] in response.json().values(), (
            f"При передаче пустых полей на `{self.login_url}` "
            "должен возвращаться текст ошибки "
            f"`{msg.FIELD_CANNOT_BE_BLANK_MSG}`."
        )

    @pytest.mark.parametrize(
        "email,password",
        [
            ("nonexistentemail@test.ru", "alskdj01"),
            ("testone@test.ru", "wrongpasswd"),
        ],
        ids=["nonexistent_email", "wrong_password"],
    )
    def test_auth_incorrect_data(self, client, user, email, password):
        """Проверка ввода несуществующего email или неверного пароля."""
        response = client.post(
            self.login_url,
            data={"email": email, "password": password},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"При передаче неверных данных на `{self.login_url}` "
            f"должен возвращаться статус {HTTPStatus.BAD_REQUEST}, а не "
            f"{response.status_code}."
        )
        assert [msg.INVALID_CREDENTIALS_MSG] in response.json().values(), (
            f"При передаче неверных данных на `{self.login_url}` должен "
            f"возвращаться текст ошибки `{msg.INVALID_CREDENTIALS_MSG}`."
        )

    def test_auth_logout(self, user_client):
        """Проверка выхода из аккаунта."""
        response = user_client.post(self.logout_url)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f"При передаче неверных данных на `{self.logout_url}` "
            f"должен возвращаться статус {HTTPStatus.NO_CONTENT}, а не "
            f"{response.status_code}."
        )

        users_me_response = user_client.get(self.user_profile_url)
        assert users_me_response.status_code == HTTPStatus.UNAUTHORIZED, (
            "При выходе из аккаунта при попытке доступа к ресурсам, "
            "требующим аутентификации, должен возвращаться статус "
            f"{HTTPStatus.UNAUTHORIZED}, а не {users_me_response.status_code}."
        )

    def test_auth_authenticated_user(self, user_client):
        """У аутентифицированного пользователя должен быть доступ."""
        users_me_response = user_client.get(self.user_profile_url)
        assert users_me_response.status_code == HTTPStatus.OK, (
            "При обращении аутентифицированного пользователя к ресурсу "
            f"`{self.user_profile_url}` должен возвращаться статус "
            f"{HTTPStatus.OK}, а вернулся {users_me_response.status_code}."
        )

    def test_auth_unauthenticated_user(self, client):
        """У анонимного пользователя не должно быть доступа."""
        users_me_response = client.get(self.user_profile_url)
        assert users_me_response.status_code == HTTPStatus.UNAUTHORIZED, (
            "При обращении неаутентифицированного пользователя к ресурсу "
            f"`{self.user_profile_url}` должен возвращаться статус "
            f"{HTTPStatus.UNAUTHORIZED}, а вернулся "
            f"{users_me_response.status_code}."
        )
