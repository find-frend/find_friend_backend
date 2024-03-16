# Generated by Django 5.0.2 on 2024-03-13 11:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_friendship_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Blacklist",
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
                (
                    "blocked_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blocked",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Блокирован",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blocker",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Черный список",
                "verbose_name_plural": "Черные списки",
            },
        ),
        migrations.AddConstraint(
            model_name="blacklist",
            constraint=models.UniqueConstraint(
                fields=("user", "blocked_user"), name="Unique_Blacklist"
            ),
        ),
    ]
