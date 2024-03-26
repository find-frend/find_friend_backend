from django.contrib import admin

from admin_auto_filters.filters import AutocompleteFilter

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    """Админка чатов."""

    list_display = (
        "id",
        "initiator",
        "receiver",
        "start_time",
    )
    list_filter = ("start_time",)
    search_fields = (
        "initiator__first_name",
        "initiator__last_name",
        "receiver__first_name",
        "receiver__last_name",
    )
    ordering = ("-start_time",)
    empty_value_display = "-пусто-"


class SenderFilter(AutocompleteFilter):
    """Фильтр сообщений по отправителю в админке."""

    title = "Отправитель"
    field_name = "sender"
    use_pk_exact = False


class ChatFilter(AutocompleteFilter):
    """Фильтр сообщений по чату в админке."""

    title = "Чат"
    field_name = "chat"
    use_pk_exact = False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Админка сообщений."""

    list_display = (
        "id",
        "sender",
        "text",
        "chat",
        "timestamp",
    )
    list_filter = ("timestamp", ChatFilter, SenderFilter)
    ordering = ("-timestamp",)
    empty_value_display = "-пусто-"
