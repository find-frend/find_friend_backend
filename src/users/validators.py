from datetime import date

from django.core.exceptions import ValidationError
from django.utils import timezone

from config.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_PASSWORD,
    MAX_USER_AGE,
    MIN_LENGTH_EMAIL,
    MIN_LENGTH_PASSWORD,
    MIN_USER_AGE,
    messages,
)


class PasswordLengthValidator:
    """Валидация длины пароля."""

    def __init__(
        self,
        min_length=MIN_LENGTH_PASSWORD,
        max_length=MAX_LENGTH_PASSWORD,
    ):
        self.min_length = min_length
        self.max_length = max_length

    def get_help_text(self, password=None, user=None):
        """Вывод требования длины пароля."""
        return messages.PASSWORD_LENGTH_MSG

    def validate(self, password, user=None):
        """Валидация длины пароля."""
        if not self.min_length <= len(password) <= self.max_length:
            raise ValidationError(
                messages.PASSWORD_LENGTH_MSG,
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

    start_date = date(now_year - MAX_USER_AGE, now_month, now_day)
    end_date = date(now_year - MIN_USER_AGE, now_month, now_day)

    if birthday > now.date():
        raise ValidationError(messages.INVALID_BIRTHDAY)
    if birthday >= end_date:
        raise ValidationError(messages.LESS_THAN_MIN_AGE)
    if birthday <= start_date:
        raise ValidationError(messages.MORE_THAN_MAX_AGE)
    return birthday


def validate_email(email):
    """Валидация почты."""
    if any(ord(char) > 127 for char in email):
        raise ValidationError(messages.EMAIL_ENGLISH_ONLY_MSG)

    if len(email) < MIN_LENGTH_EMAIL or len(email) > MAX_LENGTH_EMAIL:
        raise ValidationError(messages.EMAIL_LENGTH_MSG)

    if not email.strip():
        raise ValidationError(messages.EMPTY_FIELD_MSG)

    return email


def validate_password(password):
    """Валидация пароля."""
    if (
        len(password) < MIN_LENGTH_PASSWORD
        or len(password) > MAX_LENGTH_PASSWORD
    ):
        raise ValidationError(messages.PASSWORD_LENGTH_MSG)

    if not password.strip():
        raise ValidationError(messages.EMPTY_FIELD_MSG)

    return password
