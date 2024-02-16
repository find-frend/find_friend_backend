from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from users.models import Profile


class UserFilter(filters.FilterSet):
    """Класс фильтрации по интересам."""

    interests = filters.AllValuesMultipleFilter(field_name='interests__name')

    class Meta:
        model = Profile
        fields = ["age", "sex", "city", "interests", "profession"]


class UserSearchFilter(SearchFilter):
    """Класс поиска по имени пользователя."""

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get("name", "")
        return queryset.filter(name__startswith=name) if name else queryset
