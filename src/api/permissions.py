from rest_framework import permissions


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
        return obj.author == request.user or request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка доступа."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_admin
        )
