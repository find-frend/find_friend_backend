# Generated by Django 5.0.2 on 2024-02-23 06:17

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="City",
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
                    "name",
                    models.CharField(
                        max_length=150,
                        unique=True,
                        verbose_name="Название города",
                    ),
                ),
            ],
            options={
                "verbose_name": "Город",
                "verbose_name_plural": "Города",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Interest",
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
                    "name",
                    models.CharField(
                        max_length=150, verbose_name="Название интереса"
                    ),
                ),
                (
                    "counter",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Счётчик популярности интереса"
                    ),
                ),
            ],
            options={
                "verbose_name": "Интерес",
                "verbose_name_plural": "Интересы",
                "ordering": ["-counter"],
            },
        ),
        migrations.CreateModel(
            name="User",
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
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        verbose_name="Электронная почта",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_user_first_name",
                                message="Введены недопустимые символы.",
                                regex="^[а-яА-ЯёЁa-zA-Z]+(\\s?\\-?[а-яА-ЯёЁa-zA-Z]+){0,5}$",
                            ),
                            django.core.validators.MinLengthValidator(
                                limit_value=2
                            ),
                        ],
                        verbose_name="Имя",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_user_last_name",
                                message="Введены недопустимые символы.",
                                regex="^[а-яА-ЯёЁa-zA-Z]+(\\s?\\-?[а-яА-ЯёЁa-zA-Z]+){0,5}$",
                            ),
                            django.core.validators.MinLengthValidator(
                                limit_value=2
                            ),
                        ],
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "birthday",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[users.validators.validate_birthday],
                        verbose_name="День рождения",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        upload_to="images/user/",
                        verbose_name="Аватарка",
                    ),
                ),
                (
                    "profession",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Работа"
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        blank=True,
                        choices=[("М", "Mужчина"), ("Ж", "Женщина")],
                        help_text="Введите свой пол",
                        max_length=1,
                        verbose_name="Пол",
                    ),
                ),
                (
                    "purpose",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        verbose_name="Цель поиска друга",
                    ),
                ),
                (
                    "network_nick",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        verbose_name="Ник в других соц.сетях",
                    ),
                ),
                (
                    "additionally",
                    models.TextField(
                        blank=True, max_length=500, verbose_name="О себе"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        blank=True,
                        help_text="Город проживания",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.city",
                        verbose_name="Город",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Friend",
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
                ("is_added", models.BooleanField(default=False)),
                (
                    "friend",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friend",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "initiator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Друг",
                "verbose_name_plural": "Друзья",
            },
        ),
        migrations.AddField(
            model_name="user",
            name="friends",
            field=models.ManyToManyField(
                blank=True,
                help_text="Друзья пользователя",
                through="users.Friend",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Друзья",
            ),
        ),
        migrations.CreateModel(
            name="UserInterest",
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
                    "interest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.interest",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь-интерес",
                "verbose_name_plural": "Пользователи-интересы",
            },
        ),
        migrations.AddField(
            model_name="user",
            name="interests",
            field=models.ManyToManyField(
                blank=True,
                help_text="Интересы пользователя",
                through="users.UserInterest",
                to="users.interest",
                verbose_name="Интересы",
            ),
        ),
        migrations.AddConstraint(
            model_name="friend",
            constraint=models.UniqueConstraint(
                fields=("initiator", "friend"), name="unique_friend"
            ),
        ),
        migrations.AddConstraint(
            model_name="userinterest",
            constraint=models.UniqueConstraint(
                fields=("user", "interest"), name="unique_user_interest"
            ),
        ),
    ]
