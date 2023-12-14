from rest_framework.permissions import BasePermission


class IsOwnerOrRecipient(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.request_from_user or request.user == obj.book.owner:
            return True

        return False
