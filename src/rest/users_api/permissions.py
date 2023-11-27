from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            return bool(
                request.user.id == obj.id
                and request.user.is_staff
                or request.user.is_superuser
            )
