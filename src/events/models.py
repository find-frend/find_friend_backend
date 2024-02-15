from django.db import models

from config.settings import MAX_LENGTH_CHAR
from users.models import Profile


class Interest(models.Model):
    """Модель интересов."""

    name = models.CharField(
        max_length=MAX_LENGTH_CHAR, verbose_name="Название интереса"
    )
    counter = models.PositiveIntegerField(
        default=0, verbose_name="Счётчик популярности интереса"
    )

    class Meta:
        verbose_name = "Интерес"
        verbose_name_plural = "Интересы"
        ordering = ["-counter"]

    def __str__(self):
        return self.name


class Event(models.Model):
    """Модель мероприятия."""

    name = models.CharField(
        max_length=MAX_LENGTH_CHAR, verbose_name="Название мероприятия"
    )
    description = models.TextField(verbose_name="Описание мероприятия")
    interests = models.ManyToManyField(
        Interest, verbose_name="Интересы мероприятия"
    )
    event_type = models.CharField(
        max_length=MAX_LENGTH_CHAR, verbose_name="Тип мероприятия"
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


class EventMember(models.Model):
    """Модель связи мероприятия и участников."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_organizer = models.BooleanField()
