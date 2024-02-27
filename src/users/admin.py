from datetime import date, timedelta

from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import City, Friend, Interest, User


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Админка городов."""

    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    """Админка интересов."""

    search_fields = ("name",)
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


def years_count(value):
    """Вычисление интервала лет."""
    value = int(value)
    now = timezone.now()
    start_year = now.year - value - 10
    end_year = start_year + 10
    return start_year, end_year


class AgeFilter(admin.SimpleListFilter):
    """Фильтр пользователей по возрасту в админке."""

    title = "Возраст"
    parameter_name = "age"

    def lookups(self, request, model_admin):
        """Метод формирования списка интервалов по возрасту."""
        return [
            ("14", "14-20 лет"),
            ("20", "20-30 лет"),
            ("30", "30-40 лет"),
            ("40", "40-50 лет"),
            ("50", "50-60 лет"),
            ("60", "60-70 лет"),
            ("70", "70-80 лет"),
            ("80", "80-90 лет"),
            ("90", "90-100 лет"),
            ("100", "100-110 лет"),
            ("110", "110-120 лет"),
        ]

    def queryset(self, request, queryset):
        """Метод фильтрации пользователей по возрасту в интервале."""
        if not self.value():
            return queryset
        value = self.value()
        now = timezone.now()
        if value == "14":
            start_year = now.year - 20
            end_year = start_year + 6
        else:
            start_year, end_year = years_count(value)
        start_date = date(start_year, now.month, now.day)
        end_date = date(end_year, now.month, now.day) - timedelta(1)
        return queryset.filter(
            birthday__gte=start_date, birthday__lte=end_date
        )


class CityFilter(AutocompleteFilter):
    """Фильтр пользователей по городу в админке."""

    title = "Город"
    field_name = "city"


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
        # "email",
        "is_staff",
        "is_active",
        "sex",
        AgeFilter,
        CityFilter,
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
    ordering = ("-id",)
    empty_value_display = "-пусто-"
    search_fields = ("email", "first_name", "last_name")
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
        return obj.age()

    @admin.display(description="Количество друзей", empty_value=0)
    def friends_count(self, obj):
        """Отображение количества друзей."""
        return obj.friends_count()


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    """Админка друга пользователя."""

    list_display = (
        "initiator",
        "friend",
        "is_added",
    )
