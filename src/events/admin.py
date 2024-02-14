from itertools import chain

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Event, EventMember, Interest


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    """Админка интересов."""

    list_display = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Админка мероприятия."""

    list_display = (
        "name",
        "preview",
        "description",
        "interest_names",
        "event_type",
        "date",
        "location",
    )
    search_fields = ("name",)
    list_filter = (
        "location",
        "name",
        "interests",
    )

    @admin.display(description="Интересы")
    def interest_names(self, object):
        """Отображается название интересов."""
        interests = object.interests.values_list("name")
        return list(chain.from_iterable(interests))

    @admin.display(description="Фото мерприятия", empty_value="Нет фото")
    def preview(self, object):
        """Отображается фото мерприятия."""
        if object.image:
            print(True)
            return mark_safe(
                f'<img src="{object.image.url}" '
                'style="max-height: 100px; max-width: 100px">'
            )
        return None


@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    """Админка связи пользователей и мероприятий."""

    list_display = (
        "event",
        "profile",
        "is_organizer",
    )
