from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.applications.book_requests.models import BookRequest
from src.applications.book_requests.serializers import (
    BookRequestDetailSerializer, BookRequestListSerializer)
from src.applications.book_requests.tasks import (
    send_email_about_success_request, send_notification_about_request)
from src.applications.books.models import Book
from src.applications.users.decorators import is_object_owner

from .logic import check_if_request_exists
from .permissions import IsOwnerOrRecipient


class BookRequestViewSet(viewsets.ModelViewSet):
    queryset = BookRequest.objects.all()
    http_method_names = ["get", "post"]
    serializer_class = BookRequestListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(request_from_user=self.request.user)

    def get_queryset(self):
        if self.action == "list":
            return BookRequest.objects.filter(
                Q(book__owner=self.request.user)
                | Q(request_from_user=self.request.user)
            )

        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            return BookRequestDetailSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsOwnerOrRecipient()]
        return super().get_permissions()
