from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_birthday(birthday):

    now = timezone.now()
    if birthday > now.date():
        raise ValidationError('Birthday is greater than the current date')
    if (now.year - birthday.year) > 120:
        raise ValidationError('Age over 120 years!')
    return birthday
