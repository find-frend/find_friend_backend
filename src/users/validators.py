from django.core.exceptions import ValidationError
from django.utils import timezone

from config import settings

INVALID_SYMBOLS_MSG = "Введены недопустимые символы."
INVALID_EMAIL_MSG = "Некорректный адрес электронной почты."
FIRST_NAME_LENGTH_MSG = (
    f"Имя должно содержать от {settings.MIN_LENGTH_CHAR} до "
    f"{settings.MAX_LENGTH_CHAR} символов."
)
LAST_NAME_LENGTH_MSG = (
    f"Фамилия должна содержать от {settings.MIN_LENGTH_CHAR} до "
    f"{settings.MAX_LENGTH_CHAR} символов."
)
EMAIL_LENGTH_MSG = (
    f"Почта должна содержать от {settings.MIN_LENGTH_EMAIL} до "
    f"{settings.MAX_LENGTH_EMAIL} символов."
)


class PasswordLengthValidator:
    """Валидация длины пароля."""

    def __init__(
        self,
        min_length=settings.MIN_LENGTH_PASSWORD,
        max_length=settings.MAX_LENGTH_PASSWORD,
    ):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):
        """Валидация длины пароля."""
        if not self.min_length <= len(password) <= self.max_length:
            raise ValidationError(
                (
                    f"Пароль должен содержать от {self.min_length} "
                    f"до {self.max_length} символов."
                ),
                code="password_too_short",
            )


def validate_birthday(birthday):
    """Проверка, что год рождения не меньше 14 и не больше 120 лет."""
    now = timezone.now()
    if (now.year - birthday.year) < 14:
        raise ValidationError(
            "Указанный возраст меньше 14 лет! Проверьте дату рождения."
        )
    if (now.year - birthday.year) > 120:
        raise ValidationError(
            "Возраст больше 120 лет! Проверьте дату рождения."
        )
    return birthday
