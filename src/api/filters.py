from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from events.models import Event
from users.models import User


class UserFilter(filters.FilterSet):
    """Класс фильтрации пользователей по интересам."""

    interests = filters.AllValuesMultipleFilter(field_name="interests__name")

    class Meta:
        model = User
        fields = [
            "sex",
            "city",
            "interests",
            "profession",
            "character",
            "purpose",
        ]


class EventsFilter(filters.FilterSet):
    """Класс фильтрации мероприятий по интересам."""

    interests = filters.AllValuesMultipleFilter(field_name="interests__name")

    class Meta:
        model = Event
        fields = ["event_type", "date", "location"]


class EventSearchFilter(SearchFilter):
    """Класс поиска по названию мероприятия."""

    def filter_queryset(self, request, queryset, view):
        """Выборка по названию мероприятия."""
        name = request.query_params.get("name", "")
        return queryset.filter(name__startswith=name) if name else queryset
