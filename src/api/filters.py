from datetime import date

from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from events.models import Event
from users.models import User


class UserFilter(filters.FilterSet):
    """Класс фильтрации пользователей."""

    interests = filters.AllValuesMultipleFilter(field_name="interests__name")
    age = filters.NumberFilter(field_name="age", method="filter_age")

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "sex",
            "age",
            "city",
            "interests",
            "profession",
            "purpose",
        ]

    def filter_age(self, queryset, param, value):
        """Метод фильтрации пользователей по возрасту."""
        if not param or not value:
            return queryset
        value = int(value)
        now = timezone.now()
        now_day = now.day
        now_month = now.month
        now_year = now.year
        if now_month == 2 and now_day == 29:
            now_day -= 1
        start_date = date(now_year - value - 1, now_month, now_day)
        end_date = date(now_year - value, now_month, now_day)
        return queryset.filter(
            birthday__gte=start_date, birthday__lte=end_date
        )


class EventsFilter(filters.FilterSet):
    """Класс фильтрации мероприятий."""

    interests = filters.AllValuesMultipleFilter(field_name="interests__name")

    class Meta:
        model = Event
        fields = ["event_type", "date", "city"]


class EventSearchFilter(SearchFilter):
    """Класс поиска по названию мероприятия."""

    def filter_queryset(self, request, queryset, view):
        """Выборка по названию мероприятия."""
        name = request.query_params.get("name", "")
        return queryset.filter(name__startswith=name) if name else queryset
