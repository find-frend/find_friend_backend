from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from users.models import User


class UserFilter(filters.FilterSet):
    """Класс фильтрации по интересам."""

    interests = filters.AllValuesMultipleFilter(field_name='interests__name')

    class Meta:
        model = User
        fields = ["sex", "city", "interests", "profession"]


class UserSearchFilter(SearchFilter):
    """Класс поиска по имени пользователя."""

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get("name", "")
        return queryset.filter(
            first_name__startswith=name) if name else queryset