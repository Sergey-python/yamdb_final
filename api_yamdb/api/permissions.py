from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from users.models import User


class IsAdminUser(IsAuthenticated):
    """
    Permission предоставляющий доступ только администратору.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.role == User.ADMIN or request.user.is_superuser
        )


class IsAdminOrReadOnly(IsAdminUser):
    """
    Permission предоставляющий ограниченный доступ.
    Для чтения любым пользователям.
    Для создания, изменения и удаления только администратору.
    """

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            or request.method in SAFE_METHODS
        )


class IsStaffOrAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Permission предоставляющий ограниченный доступ.
    Для чтения любым пользователям.
    Для создания, изменения и удаления только администратору,
    модератору и автору.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.role == User.MODERATOR
            or request.user.role == User.ADMIN
        )
