from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import Friend, Profile, User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """Админка пользователя."""

    model = User
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    empty_value_display = "-пусто-"


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    """Админка друга пользователя."""

    list_display = (
        "initiator",
        "friend",
        "is_added",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Админка профиля пользователя."""

    model = Profile
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "nickname",
        "age",
        "interests",
        "city",
        "preview",
        "profession",
        "character",
        "sex",
        "purpose",
        "network_nick",
        "additionally",
    )
    search_fields = ("nickname", "first_name", "last_name")
    ordering = ("nickname",)
    readonly_fields = ["preview"]

    @admin.display(description="Фото профиля", empty_value="Нет фото")
    def preview(self, obj):
        """Отображение аватара профиля."""
        if obj.avatar:
            return mark_safe(
                f"""<img src='{obj.avatar.url}'
                 style="max-height: 100px; max-width: 100px">'"""
            )
        return None
