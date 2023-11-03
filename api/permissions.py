from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


UPDATE_METHODS = ("PUT", "PATCH")


class IsOwnerOrStaffOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST" and request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method in UPDATE_METHODS and request.user == obj.owner:
            return True

        return False
