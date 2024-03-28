from decimal import Decimal

from django.db import models
from django.utils import timezone

from config.constants import MAX_LENGTH_CHAR, MAX_LENGTH_EVENT
from users.models import City, Interest, User


class Event(models.Model):
    """Модель мероприятия."""

    name = models.CharField(
        max_length=MAX_LENGTH_EVENT, verbose_name="Название мероприятия"
    )
    description = models.TextField(verbose_name="Описание мероприятия")
    """    interests = models.ManyToManyField(
        Interest,
        through="EventInterest",
        verbose_name="Интересы",
        help_text="Интересы мероприятия",
    )
    """
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
        default=Decimal("0.00"),
        verbose_name="Стоимость мероприятия",
    )
    start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата начала",
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата окончания",
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Место проведения",
    )
    address = models.CharField(
        max_length=MAX_LENGTH_CHAR,
        verbose_name="Улица, дом",
        help_text="Введите тип и название улицы, номер дома",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="images/events/",
        verbose_name="Фото мероприятия",
        blank=True,
        null=True,
    )
    min_age = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Минимальный возраст участников",
    )
    max_age = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Максимальный возраст участников",
    )
    min_count_members = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Минимальное количество участников",
    )
    max_count_members = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Максимальное количество участников",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date"))
                | models.Q(end_date__isnull=True),
                name="date_event_constraint",
            ),
        ]
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ("-start_date",)

    def __str__(self):
        return self.name

    def members_count(self):
        """Получение числа участников мероприятия."""
        return self.members.count()


class EventInterest(models.Model):
    """Модель связи мероприятия и интересов."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)


class EventMember(models.Model):
    """Модель связи мероприятия и участников."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
    )
    is_organizer = models.BooleanField()

    class Meta:
        verbose_name = "Участники мероприятия"
        verbose_name_plural = "Участники мероприятия"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "event",
                    "user",
                ],
                name="unique_member",
            )
        ]


class EventLocation(models.Model):
    """Модель хранения геолокации мероприятий."""

    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, verbose_name="Мероприятие"
    )
    lon = models.DecimalField(
        verbose_name="Долгота", max_digits=9, decimal_places=6
    )
    lat = models.DecimalField(
        verbose_name="Широта", max_digits=9, decimal_places=6
    )

    class Meta:
        verbose_name = "Геолокация мероприятия"
        verbose_name_plural = "Геолокация мероприятий"

    def __str__(self):
        return f"{self.event} {self.lat}:{self.lon}"


class EventRequest(models.Model):
    """Модель заявки на участие в мероприятии."""

    STATUS_CHOICES = (
        ("Pending", "В ожидании"),
        ("Accepted", "Принято"),
        ("Declined", "Отклонено"),
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_event_requests",
        verbose_name="Инициатор",
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_event_requests",
        verbose_name="Организатор",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_request",
        verbose_name="Мероприятие",
    )
    status = models.CharField(
        max_length=MAX_LENGTH_CHAR,
        choices=STATUS_CHOICES,
        default="Pending",
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Создано"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "from_user",
                    "event",
                ],
                name="unique_event_member",
            )
        ]

        ordering = ["-created_at"]
        verbose_name = "Заявка на мероприятие"
        verbose_name_plural = "Заявки на мероприятия"

    def __str__(self):
        return f"{self.from_user}: {self.event.name}"
