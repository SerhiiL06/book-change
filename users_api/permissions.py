from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedAndOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        if request.method == "DELETE" and request.user.is_superuser:
            return True
