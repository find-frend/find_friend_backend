from django.core.exceptions import ValidationError
from django.utils import timezone


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
