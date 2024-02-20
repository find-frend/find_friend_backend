from decimal import Decimal

from django.db import models

from config.settings import MAX_LENGTH_CHAR, MAX_LENGTH_EVENT
from users.models import Interest, User


class Event(models.Model):
    """Модель мероприятия."""

    name = models.CharField(
        max_length=MAX_LENGTH_EVENT, verbose_name="Название мероприятия"
    )
    description = models.TextField(verbose_name="Описание мероприятия")
    '''    interests = models.ManyToManyField(
        Interest,
        through="EventInterest",
        verbose_name="Интересы",
        help_text="Интересы мероприятия",
    )
    '''
    members = models.ManyToManyField(
        User,
        through="EventMember",
        verbose_name="Участники",
        help_text="Участники мероприятия",
    )
    event_type = models.CharField(
        max_length=MAX_LENGTH_EVENT, verbose_name="Тип мероприятия"
    )
    event_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Стоимость мероприятия"
    )
    date = models.DateTimeField(
        verbose_name="Дата мероприятия",
    )
    location = models.CharField(
        max_length=MAX_LENGTH_CHAR, verbose_name="Место проведения мероприятия"
    )
    image = models.ImageField(
        upload_to="images/events/", verbose_name="Фото мероприятия", blank=True
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ("-date",)

    def __str__(self):
        return self.name


class EventInterest(models.Model):
    """Модель связи мероприятия и интересов."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)


class EventMember(models.Model):
    """Модель связи мероприятия и участников."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_organizer = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "event",
                    "user",
                ],
                name="unique_member",
            )
        ]
