# Generated by Django 5.0.2 on 2024-02-20 11:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_event_event_price_alter_event_event_type_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="interests",
        ),
        migrations.AddField(
            model_name="event",
            name="members",
            field=models.ManyToManyField(
                help_text="Участники мероприятия",
                through="events.EventMember",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Участники",
            ),
        ),
        migrations.AddConstraint(
            model_name="eventmember",
            constraint=models.UniqueConstraint(
                fields=("event", "user"), name="unique_member"
            ),
        ),
        migrations.AddConstraint(
            model_name="eventmember",
            constraint=models.UniqueConstraint(
                fields=("user", "is_organizer"), name="unique_organizer"
            ),
        ),
    ]
