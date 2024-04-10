from rest_framework import permissions

from events.models import ParticipationRequest
from users.models import User


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """Проверка доступа."""

    def has_permission(self, request, view):
        """Проверка доступа."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Проверка доступа."""
        if request.method == "GET":
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return obj.id == request.user.id or request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка доступа."""

    def has_permission(self, request, view):
        """Проверка доступа."""
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_staff
        )


class IsRecipient(permissions.BasePermission):
    """Проверка разрешения, что текущий пользователь является.

    получателем заявки на дружбу.
    """

    def has_object_permission(self, request, view, obj):
        """Возвращает True.

        Eсли текущий пользователь является получателем заявки на дружбу.
        """
        return obj.to_user == request.user


class IsEventOrganizer(permissions.BasePermission):
    """Проверка того, что текущий пользователь является организатором.

    мероприятия. Для обработки заявок на участие в мероприятии.
    """

    def has_permission(self, request, view):
        """Проверка доступа. Возвращает  True.

        Eсли текущий пользователь является организатором мероприятия.
        """
        event = int(view.kwargs["pk"])
        participation = ParticipationRequest.objects.get(pk=event)
        organizer = User.objects.get(
            user__is_organizer=True, user__event=participation.event
        )
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == organizer
        )


class IsAdminOrAuthorOrReadOnlyAndNotBlocked(permissions.BasePermission):
    """Проверка доступа."""

    def has_permission(self, request, view):
        """Проверка доступа."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Проверка доступа."""
        if request.method == "GET":
            if not (
                obj.id == request.user.id or request.user.is_staff
            ) and request.user.is_blocked(obj):
                return False
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return obj.id == request.user.id or request.user.is_staff
