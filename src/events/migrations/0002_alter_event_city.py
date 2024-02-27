# Generated by Django 5.0.2 on 2024-02-24 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="city",
            field=models.ForeignKey(
                max_length=150,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.city",
                verbose_name="Место проведения мероприятия",
            ),
        ),
    ]
