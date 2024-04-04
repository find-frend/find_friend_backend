from http import HTTPStatus

import pytest

from config import constants as cnst
from config.constants import messages as msg

from .test_auth import generate_long_email, generate_long_string


@pytest.mark.django_db(transaction=True)
class TestUserRegisterAPI:
    """Тесты регистрации пользователей."""

    users_url = "/api/v1/users/"

    data = {
        "first_name": "Новый",
        "last_name": "Юзер",
        "password": "validpasswd",
        "email": "validemail@test.ru",
    }

    def test_register_correct_data(self, client):
        """Проверка успешной регистрации при вводе корректных данных."""
        response = client.post(self.users_url, self.data)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f"Страница `{self.users_url}` не найдена, проверьте этот адрес "
            "в *urls.py*"
        )

        assert (
            response.status_code == HTTPStatus.CREATED
        ), f"Страница `{self.users_url}` работает неправильно!"

        register_data = response.json()
        assert all(
            field in register_data
            for field in ["first_name", "last_name", "email"]
        ), (
            f"Проверьте, что при POST запросе на `{self.users_url}` "
            "возвращается объект пользователя."
        )

    def test_register_existing_user(self, client, user):
        """Проверка регистрации существующего пользователя."""
        data = self.data.copy()
        data["email"] = user.email
        response = client.post(self.users_url, data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"Проверьте, что при POST запросе на `{self.users_url}` "
            "при попытке регистрации существующего пользователя "
            f"возвращается статус {HTTPStatus.BAD_REQUEST}."
        )

    @pytest.mark.parametrize(
        "email,error_text",
        [
            ("invalidemail.ru", msg.INVALID_EMAIL_MSG),
            (
                generate_long_email(cnst.MAX_LENGTH_EMAIL + 1),
                msg.EMAIL_LENGTH_MSG,
            ),
            ("wrong<>symbols@test.ru", msg.INVALID_EMAIL_MSG),
        ],
        ids=["invalid_format", "too_long", "wrong_symbols"],
    )
    def test_register_invalid_email(self, client, email, error_text):
        """Проверка регистрации с электронной почтой в некорректном формате."""
        data = self.data.copy()
        data["email"] = email
        response = client.post(self.users_url, data)
        assert error_text == response.json()["email"][0], (
            f"При регистрации с почтой {email} "
            f"должен возвращаться текст ошибки `{error_text}`, "
            f"а вернулся `{response.json()['email'][0]}`."
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"При регистрации с почтой {email} "
            f"должен возвращаться статус {HTTPStatus.BAD_REQUEST}, "
            f"а был возвращен {response.status_code}."
        )

    @pytest.mark.parametrize(
        "password,error_text",
        [
            ("p", msg.PASSWORD_LENGTH_MSG),
            (
                generate_long_string(cnst.MAX_LENGTH_PASSWORD + 1),
                msg.PASSWORD_LENGTH_MSG,
            ),
            ("81672049", msg.password_numeric_msg),
            ("qwerty123", msg.password_common_msg),
        ],
        ids=[
            "too_short",
            "too_long",
            "only_digits",
            "too_common",
        ],
    )
    def test_resgiter_invalid_password(self, client, password, error_text):
        """Проверка регистрации с паролем в некорректном формате."""
        data = self.data.copy()
        data["password"] = password
        response = client.post(self.users_url, data)
        assert error_text == response.json()["password"][0], (
            f"При передаче {password} на `{self.users_url}` "
            f"должен возвращаться текст ошибки `{error_text}`, "
            f"а вернулся `{response.json()['password'][0]}`."
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"При передаче {password} на `{self.users_url}` "
            f"должен возвращаться статус {HTTPStatus.BAD_REQUEST}, "
            f"а был возвращен {response.status_code}."
        )

    @pytest.mark.parametrize(
        "field,value,error_text",
        [
            ("first_name", "F", msg.FIRST_NAME_LENGTH_MSG),
            ("last_name", "L", msg.LAST_NAME_LENGTH_MSG),
            (
                "first_name",
                generate_long_string(cnst.MAX_LENGTH_CHAR + 1),
                msg.FIRST_NAME_LENGTH_MSG,
            ),
            (
                "last_name",
                generate_long_string(cnst.MAX_LENGTH_CHAR + 1),
                msg.LAST_NAME_LENGTH_MSG,
            ),
            ("first_name", "123", msg.INVALID_SYMBOLS_MSG),
            ("last_name", "<>", msg.INVALID_SYMBOLS_MSG),
        ],
        ids=[
            "short_first_name",
            "short_last_name",
            "long_first_name",
            "long_last_name",
            "invalid_symbols_first_name",
            "invalid_symbols_last_name",
        ],
    )
    def test_register_name(self, client, field, value, error_text):
        """Проверка регистрации с некорректными именем и фамилией."""
        data = self.data.copy()
        data[field] = value
        response = client.post(self.users_url, data)
        assert error_text == response.json()[field][0], (
            f"При передаче {value} в качестве значения поля {field} на "
            f"`{self.users_url}` должен возвращаться текст ошибки "
            f"{error_text}`, а вернулся `{response.json()[field][0]}`."
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"При передаче {value} в качестве значения поля {field} на "
            f"`{self.users_url}` должен возвращаться статус "
            f"{HTTPStatus.BAD_REQUEST}, а вернулся {response.status_code}."
        )

    @pytest.mark.parametrize(
        "field",
        ["email", "password", "first_name", "last_name"],
        ids=[
            "empty_email",
            "empty_password",
            "empty_first_name",
            "empty_last_name",
        ],
    )
    def test_register_empty_fields(self, client, field):
        """Проверка регистрации с пустыми полями."""
        data = self.data.copy()
        data[field] = " "
        response = client.post(self.users_url, data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"При передаче пустых полей на `{self.users_url}` "
            f"должен возвращаться статус {HTTPStatus.BAD_REQUEST}, а не "
            f"{response.status_code}."
        )
        assert [msg.FIELD_CANNOT_BE_BLANK_MSG] in response.json().values(), (
            f"При передаче пустых полей на `{self.users_url}` "
            "должен возвращаться текст ошибки "
            f"`{msg.FIELD_CANNOT_BE_BLANK_MSG}`."
        )
