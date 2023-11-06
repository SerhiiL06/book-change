from django_filters import rest_framework as filter
from rest_framework import filters, permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from books.models import Book, Genre
from books.serializers import (BookListSerializer, BookSerializer,
                               GenreSerializer)
from users.models import User
from users.serializers import UserSerializer

from .permissions import IsOwnerOrStaffOrSuperuser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrStaffOrSuperuser]
    serializer_class = UserSerializer
    filter_backends = [
        filter.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["my_books", "email"]
    ordering_fields = "__all__"
    search_fields = ["email"]

    def get_object(self):
        return super().get_object()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrStaffOrSuperuser]
    filter_backends = [filter.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["id", "genre__title", "owner__first_name", "author"]
    order_fields = ["title", "rating"]
    search_fields = ["title", "owner", "author"]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return self.serializer_class
