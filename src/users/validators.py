from datetime import date

from django.core.exceptions import ValidationError
from django.utils import timezone


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
