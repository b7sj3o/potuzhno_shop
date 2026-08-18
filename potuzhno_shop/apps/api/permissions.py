from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    message = "Змінювати каталог / Фільтрувати відгуки може лише персонал магазину"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrStaffOrReadOnly(BasePermission):
    message = "Змінювати цей об'єкт може лише власник"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if hasattr(obj, "user"):
            return (obj.user == request.user) or (request.user and request.user.is_staff)
        return False
