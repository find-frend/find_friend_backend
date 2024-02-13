from django.db import models
from .constants import MAX_LENGTH_VALUE


class Interest(models.Model):

    """ Модель интересов. """

    name = models.CharField(
        max_length=MAX_LENGTH_VALUE,
        verbose_name='Название интереса'
    )

    class Meta:
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'

    def __str__(self):
        return self.name


class Event(models.Model):

    """ Модель мероприятия. """

    name = models.CharField(
        max_length=MAX_LENGTH_VALUE,
        verbose_name='Название мероприятия'
    )
    description = models.TextField(
        verbose_name='Описание мероприятия'
    )
    interests = models.ManyToManyField(
        Interest,
        verbose_name='Интересы мероприятия'
    )
    event_type = models.CharField(
        max_length=MAX_LENGTH_VALUE,
        verbose_name='Тип мероприятия'
    )
    date = models.DateTimeField(
        verbose_name='Дата мероприятия',
    )
    location = models.CharField(
        max_length=MAX_LENGTH_VALUE,
        verbose_name='Место проведения мероприятия'
    )
    image = models.ImageField(
        upload_to='events/images/',
        verbose_name='Фото мероприятия',
        blank=True
    )

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ('-date',)

    def __str__(self):
        return self.name

# class EventMember(models.Model):
#     event = models.ForeignKey(Event,
#                               on_delete=models.CASCADE)
#     profile = models.ForeignKey(Profile,
#                                 on_delete=models.CASCADE)
#     is_organizer = models.BooleanField()
