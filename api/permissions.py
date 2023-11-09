from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response

UPDATE_METHODS = ("PUT", "PATCH")


class ReadOnlyOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        if request.method == "POST" and request.user.is_staff:
            return True
        if request.method in UPDATE_METHODS and request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_staff:
            return True

        if request.method in UPDATE_METHODS and request.user == obj:
            return True

        if request.method == "DELETE" and request.user.is_staff:
            return True
