from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework import parsers
from rest_framework.decorators import action
from .permissions import OwnerOrStaff
from . import paginators
from src.applications.books.models import Author, Book, Genre, Comment
from src.applications.books.serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    GenreListSerializer,
    GenreDetailSerializer,
    BookDetailSerializer,
    BookListSerializer,
    CommentSerializer,
    UpdateCommentSerializer,
    CreateBookSerializer,
    BookUpdateSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.prefetch_related("books")
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = paginators.StandartResultPaginator
    serializer_class = AuthorDetailSerializer
    filter_backends = [filter.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        if self.action == "list":
            return Author.objects.all()
        return super().get_queryset()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return super().get_permissions()
        if self.action in ["create", "update", "destroy"]:
            return permissions.IsAdminUser

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer

        return super().get_serializer_class()


class GenreViewSets(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filter.DjangoFilterBackend]
    filterset_fields = ["title"]
    search_fields = ["title"]
    ordering_fields = ["title"]

    def get_queryset(self):
        if self.action == "retrieve":
            return Genre.objects.prefetch_related("genre_books")
        return super().get_queryset()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return super().get_permissions()
        if self.action in ["create", "update", "destroy"]:
            return permissions.IsAdminUser

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GenreDetailSerializer

        return super().get_serializer_class()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [OwnerOrStaff]
    pagination_class = paginators.BookPaginator
    parser_classes = [parsers.MultiPartParser]
    serializer_class = BookListSerializer
    http_method_names = ["get", "post", "put", "delete"]

    filter_backends = [filter.DjangoFilterBackend]
    filtersets_fields = ["owner", "author", "genre"]

    @swagger_auto_schema(
        operation_description="get all books. paramethers: owner, author, genre",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(request_body=CreateBookSerializer)
    def create(self, request, *args, **kwargs):
        data = CreateBookSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save(owner=request.user)
        return Response(status=200, data="book create")

    @swagger_auto_schema(request_body=BookUpdateSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path="my-books",
    )
    def my_books(self, request):
        books = Book.objects.filter(owner=request.user)

        serializer = BookListSerializer(instance=books, many=True)

        return Response({"my_books": serializer.data})

    def get_serializer_class(self):
        if self.action == "list":
            return super().get_serializer_class()

        if self.action == "create":
            return CreateBookSerializer

        if self.action == "update":
            return BookUpdateSerializer
        return BookDetailSerializer

    def get_permissions_classes(self):
        if self.action in ["list", "retrieve"]:
            return permissions.AllowAny

        if self.action == "create":
            return permissions.IsAuthenticated

        return super().get_permissions_classes()

    def get_queryset(self):
        if self.action == "list":
            return super().get_queryset()

        return Book.objects.prefetch_related("comments")


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "put", "delete"]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(request_body=UpdateCommentSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save(current_user=self.request.user)

    def get_permissions(self):
        if self.action == "destroy":
            return OwnerOrStaff
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UpdateCommentSerializer
        return super().get_serializer_class()
