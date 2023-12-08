from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return bool(request.user.id == obj.id or request.user.is_staff)

        return False
