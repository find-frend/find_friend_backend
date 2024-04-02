from itertools import chain

from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Event, EventLocation, EventMember, ParticipationRequest


class CityEventFilter(AutocompleteFilter):
    """Фильтр мероприятий по городу в админке."""

    title = "Место проведения"
    field_name = "city"
    use_pk_exact = False


class MemberInlineAdmin(admin.TabularInline):
    """Админка связи мероприятия и участников."""

    model = Event.members.through
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Админка мероприятия."""

    list_display = (
        "name",
        "preview",
        "description",
        "event_type",
        "start_date",
        "end_date",
        "city",
        "address",
        "event_price",
        "members_count",
        "min_age",
        "max_age",
        "min_count_members",
        "max_count_members",
    )
    list_filter = (CityEventFilter,)
    inlines = (MemberInlineAdmin,)
    search_fields = (
        "name",
        "event_type",
        "start_date",
        "city__name",
        "address",
    )
    readonly_fields = ["preview"]

    @admin.display(description="Интересы")
    def interest_names(self, object):
        """Отображается название интересов."""
        interests = object.interests.values_list("name")
        return list(chain.from_iterable(interests))

    @admin.display(description="Участники")
    def member_names(self, object):
        """Отображаются имена пользователей."""
        users = object.users.values_list("email")
        return list(chain.from_iterable(users))

    @admin.display(description="Просмотр фото", empty_value="Нет фото")
    def preview(self, object):
        """Отображается фото мероприятия."""
        if object.image:
            print(True)
            return mark_safe(
                f'<img src="{object.image.url}" '
                'style="max-height: 100px; max-width: 100px">'
            )
        return None

    @admin.display(description="Число участников")
    def members_count(self, object):
        """Отображение числа участников."""
        return object.members_count()


@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    """Админка связи пользователей и мероприятий."""

    list_display = (
        "event",
        "user",
        "is_organizer",
    )


@admin.register(EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
    """Админка для модели EventLocation."""

    list_display = (
        "event",
        "lat",
        "lon",
    )
    search_fields = ("event__name",)


@admin.register(ParticipationRequest)
class ParticipationRequestAdmin(admin.ModelAdmin):
    """Админка для модели ParticipationRequest."""

    list_display = (
        "from_user",
        "processed_by",
        "event",
        "status",
        "created_at",
        "updated_at",
        "id",
    )
    search_fields = ("event__name", "status")
    list_filter = ("status", "created_at", "updated_at")
