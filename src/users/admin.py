from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import City, Friend, Interest, User


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Админка городов."""

    list_display = ("id", "name")


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    """Админка интересов."""

    list_display = ("name",)


class InterestInlineAdmin(admin.TabularInline):
    """Админка связи пользователя и интересов."""

    model = User.interests.through
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
        "nickname",
        "birthday",
        "city",
        "profession",
        "character",
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
                    # "avatar",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    inlines = (InterestInlineAdmin,)
    search_fields = ("email", "first_name", "last_name", "nickname")
    ordering = ("-id",)
    empty_value_display = "-пусто-"
    readonly_fields = ["preview"]

    @admin.display(description="Фото профиля", empty_value="Нет фото")
    def preview(self, obj):
        """Отображение аватара профиля."""
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" '
                'style="max-height: 100px; max-width: 100px">'
            )
        return None


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    """Админка друга пользователя."""

    list_display = (
        "initiator",
        "friend",
        "is_added",
    )
