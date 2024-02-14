from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import Profile, User, Friend


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
    list_display = (
        "application_creator",
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

    def preview(self, obj):
        """Отображение аватара профиля."""
        return mark_safe(
            f"<img src='{obj.avatar.url}' width={obj.avatar.width}/>"
        )

    preview.short_description = "Изображение"

