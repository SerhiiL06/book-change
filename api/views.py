from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from users.models import User
from users.serializers import UserSerializer
from books.models import Genre, Book
from books.serializers import GenreSerializer, BookSerializer
from django_filters import rest_framework as filter
from rest_framework import filters


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer
    permission_classes = [permissions.BasePermission]
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
    filter_backends = [filter.DjangoFilterBackend]
    filterset_fields = ["id", "genre__title", "owner__first_name", "author"]
