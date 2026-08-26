from rest_framework.permissions import BasePermission, SAFE_METHODS


CATALOG_MANAGER_GROUP = "Менеджер каталогу"
REVIEW_MODERATOR_GROUP = "Модератор відгуків"


class IsCatalogManagerOrReadOnly(BasePermission):
    message = "Змінювати каталог може лише менеджер каталогу"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        return request.user.groups.filter(name=CATALOG_MANAGER_GROUP).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not hasattr(obj, "user"):
            return False

        if obj.user == request.user:
            return True

        if request.user.is_superuser:
            return True

        return request.user.groups.filter(name=CATALOG_MANAGER_GROUP).exists()


class IsReviewsModeratorOrReadOnly(BasePermission):
    message = "Змінювати відгуки може лише модератор відгуків або власник"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not hasattr(obj, "user"):
            return False

        if obj.user == request.user:
            return True

        if request.user.is_superuser:
            return True

        return request.user.groups.filter(name=REVIEW_MODERATOR_GROUP).exists()
