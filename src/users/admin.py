from datetime import date

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import City, Friend, Interest, User


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Админка городов."""

    list_display = ("name",)


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    """Админка интересов."""

    list_display = ("name",)


class InterestInlineAdmin(admin.TabularInline):
    """Админка связи пользователя и интересов."""

    model = User.interests.through
    extra = 0


class FriendInlineAdmin(admin.TabularInline):
    """Админка связи пользователя и друзей."""

    fk_name = "initiator"
    model = User.friends.through
    extra = 0


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """Админка пользователя."""

    model = User
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        # "age",
        "is_staff",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    basic_fields = (
        "email",
        "first_name",
        "last_name",
        "birthday",
        "city",
        "profession",
        "sex",
        "purpose",
        "network_nick",
        "additionally",
        "avatar",
    )
    fieldsets = (
        (
            None,
            {
                "fields": basic_fields
                + (
                    "preview",
                    "age",
                    "friends_count",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": basic_fields
                + (
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    inlines = (InterestInlineAdmin, FriendInlineAdmin)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-id",)
    empty_value_display = "-пусто-"
    readonly_fields = ["preview", "age", "friends_count"]

    @admin.display(description="Фото профиля", empty_value="Нет фото")
    def preview(self, obj):
        """Отображение аватара профиля."""
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" '
                'style="max-height: 100px; max-width: 100px">'
            )
        return None

    @admin.display(description="Возраст", empty_value=0)
    def age(self, obj):
        """Отображение возраста."""
        today = date.today()
        return (
            today.year
            - obj.birthday.year
            - (
                (today.month, today.day)
                < (obj.birthday.month, obj.birthday.day)
            )
        )

    @admin.display(description="Количество друзей", empty_value=0)
    def friends_count(self, obj):
        """Отображение количества друзей."""
        return obj.friends.count()


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    """Админка друга пользователя."""

    list_display = (
        "initiator",
        "friend",
        "is_added",
    )
