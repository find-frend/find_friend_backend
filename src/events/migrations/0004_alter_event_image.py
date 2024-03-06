# Generated by Django 5.0.2 on 2024-03-04 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_alter_event_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="images/events/",
                verbose_name="Фото мероприятия",
            ),
        ),
    ]
