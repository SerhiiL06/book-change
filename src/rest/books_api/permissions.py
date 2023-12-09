from rest_framework.permissions import BasePermission


class OwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["DELETE", "PUT"] and (
            obj.owner == request.user or request.user.is_staff
        ):
            return True
        return False
