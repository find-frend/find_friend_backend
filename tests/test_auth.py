import random
import string

import pytest


def generate_long_email(length):
    """Генерация слишком длинного адреса электронной почты."""
    local_part = "".join(
        random.choices(string.ascii_letters + string.digits, k=length - 15)
    )
    domain = "".join(random.choices(string.ascii_lowercase, k=250))
    return local_part + "@" + domain + ".com"


def generate_long_password(length):
    """Генерация слишком длинного пароля."""
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )


@pytest.mark.django_db(transaction=True)
class TestAuthAPI:
    """Тесты аутентификации."""

    login_url = "/api/v1/auth/token/login/"
    logout_url = "/api/v1/auth/token/logout/"

    def test_auth_correct_data(self, client, user):
        """Проверка успешного входа в систему при вводе корректных данных."""
        response = client.post(
            self.login_url,
            data={"email": user.email, "password": "alskdj01"},
        )

        assert response.status_code != 404, (
            f"Страница `{self.login_url}` не найдена, проверьте этот адрес "
            "в *urls.py*"
        )

        assert (
            response.status_code == 200
        ), f"Страница `{self.login_url}` работает неправильно!"

        auth_data = response.json()
        assert "auth_token" in auth_data, (
            f"Проверьте, что при POST запросе `{self.login_url}` "
            "возвращаете токен"
        )

    @pytest.mark.parametrize(
        "email,error_text,status_code",
        [
            (
                "русскиесимволы@test.ru",
                "Почта должна содержать буквы только английского алфавита.",
                400,
            ),
            ("invalidemail.ru", "Некорректный адрес электронной почты.", 400),
            ("a@a", "Почта должна содержать от 5 до 254 символов.", 400),
            (
                generate_long_email(260),
                "Почта должна содержать от 5 до 254 символов.",
                400,
            ),
            (
                "wrong<>symbols@test.ru",
                "Некорректный адрес электронной почты.",
                400,
            ),
        ],
        ids=[
            "rus_symbols",
            "invalid_format",
            "too_short",
            "too_long",
            "wrong_symbols",
        ],
    )
    def test_auth_invalid_email(self, client, email, error_text, status_code):
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

        assert response.status_code == status_code, (
            f"При передаче {email} на `{self.login_url}` "
            f"должен возвращаться статус {status_code}, "
            f"а был возвращен {response.status_code}."
        )

    @pytest.mark.parametrize(
        "password,error_text,status_code",
        [
            ("short", "Пароль должен содержать от 8 до 50 символов.", 400),
            (
                generate_long_password(51),
                "Пароль должен содержать от 8 до 50 символов.",
                400,
            ),
        ],
        ids=[
            "too_short",
            "too_long",
        ],
    )
    def test_auth_invalid_password(
        self, client, password, error_text, status_code
    ):
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

        assert response.status_code == status_code, (
            f"При передаче {password} на `{self.login_url}` "
            f"должен возвращаться статус {status_code}, "
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
        assert response.status_code == 400, (
            f"При передаче пустых полей на `{self.login_url}` "
            f"должен возвращаться статус 400, а не {response.status_code}."
        )
        assert [
            "Это поле не может быть пустым."
        ] in response.json().values(), (
            f"При передаче пустых полей на `{self.login_url}` "
            "должен возвращаться текст ошибки "
            "`Это поле не может быть пустым.`"
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
        assert response.status_code == 400, (
            f"При передаче неверных данных на `{self.login_url}` "
            f"должен возвращаться статус 400, а не {response.status_code}."
        )
        assert [
            "Невозможно войти с предоставленными учетными данными."
        ] in response.json().values(), (
            f"При передаче неверных данных на `{self.login_url}` "
            "должен возвращаться текст ошибки `Невозможно войти с "
            "предоставленными учетными данными.`"
        )

    def test_auth_logout(self, user_client):
        """Проверка выхода из аккаунта."""
        response = user_client.post(self.logout_url)
        assert response.status_code == 204, (
            f"При передаче неверных данных на `{self.login_url}` "
            f"должен возвращаться статус 204, а не {response.status_code}."
        )

        users_me_response = user_client.get("/api/v1/users/me/")
        assert users_me_response.status_code == 401, (
            "При выходе из аккаунта при попытке доступа к ресурсам, "
            "требующим аутентификации, должен возвращаться статус 401, "
            f"а не {users_me_response.status_code}."
        )
