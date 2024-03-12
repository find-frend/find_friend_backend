from datetime import date

from django.core.exceptions import ValidationError
from django.utils import timezone

from config import settings
from config.constants import messages


class PasswordLengthValidator:
    """Валидация длины пароля."""

    def __init__(
        self,
        min_length=settings.MIN_LENGTH_PASSWORD,
        max_length=settings.MAX_LENGTH_PASSWORD,
    ):
        self.min_length = min_length
        self.max_length = max_length

    def get_help_text(self, password=None, user=None):
        """Вывод требования длины пароля."""
        return (
            f"Пароль должен содержать от {self.min_length} "
            f"до {self.max_length} символов."
        )

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
    now_day = now.day
    now_month = now.month
    now_year = now.year

    if now_month == 2 and now_day == 29:
        now_day -= 1

    start_date = date(now_year - 120, now_month, now_day)
    end_date = date(now_year - 14, now_month, now_day)

    if birthday >= end_date:
        raise ValidationError(
            "Указанный возраст меньше 14 лет! Проверьте дату рождения."
        )
    if birthday <= start_date:
        raise ValidationError(
            "Возраст больше 120 лет! Проверьте дату рождения."
        )
    return birthday
