# Generated by Django 5.0.2 on 2024-02-14 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_alter_event_event_type_alter_event_image_and_more"),
        (
            "users",
            "0004_alter_profile_additionally_alter_profile_city_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="EventMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_organizer", models.BooleanField()),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.event",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.profile",
                    ),
                ),
            ],
        ),
    ]
