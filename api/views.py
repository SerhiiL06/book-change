from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from users.models import User
from .permissions import IsOwnerOrStaffOrSuperuser
from users.serializers import UserSerializer
from books.models import Genre, Book
from books.serializers import GenreSerializer, BookSerializer
from django_filters import rest_framework as filter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters


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

    # def get_serializer_class(self):
    #     if self.action == "list":
    #     return super().get_serializer_class()
