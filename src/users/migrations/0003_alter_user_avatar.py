# Generated by Django 5.0.2 on 2024-03-04 14:12

import users.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_friend_friend_alter_friend_initiator"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                upload_to="images/user/",
                validators=[users.validators.validate_size_file],
                verbose_name="Аватарка",
            ),
        ),
    ]
