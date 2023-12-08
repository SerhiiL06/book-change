from http import HTTPStatus

from rest_framework import permissions
from django_filters import rest_framework as filter
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework import viewsets
from . import paginators
from src.applications.books.models import Author, Book, Genre
from src.applications.books.serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    GenreListSerializer,
    GenreDetailSerializer,
    BookDetailSerializer,
    BookListSerializer,
    CommentSerializer,
    CreateBookSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.prefetch_related("books")
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = paginators.StandartRelustPaginator
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


class BookListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Book.objects.all()
        owner_search = request.query_params.get("owner")
        title_search = request.query_params.get("title")
        genre_search = request.query_params.get("genre")
        ordering_search = request.query_params.get("ordering")
        if owner_search:
            queryset = Book.objects.filter(owner__email=owner_search)

        if title_search:
            queryset = Book.objects.filter(title__icontains=title_search)

        if genre_search:
            queryset = Book.objects.filter(genre__title__icontains=genre_search)

        if ordering_search:
            queryset = Book.objects.all().order_by(ordering_search)

        serializer = BookListSerializer(queryset, many=True)
        return Response({"list_of_books": serializer.data})

    def post(self, request, *args, **kwargs):
        new_book = CreateBookSerializer(data=request.data)
        new_book.is_valid(raise_exception=True)
        new_book.save(owner=request.user)

        return Response({"new book": new_book.data})


class BookDetailAPIView(APIView):
    error_except = Response(
        {"Error": "Book with this ID does not exist"}, status=HTTPStatus.NOT_FOUND
    )
    dont_have_permission = Response({"error": "You don't have permissions"})

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return self.error_except
        serializer = BookDetailSerializer(book, many=False)
        return Response({"book": serializer.data})

    def patch(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return self.error_except
        if book.owner == request.user:
            serializer = BookDetailSerializer(data=request.data, instance=book)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"update is good": serializer.data})

        return self.dont_have_permission

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return self.error_except

        if book.owner == request.user or request.user.is_superuser:
            book.delete()
            return Response({"well done": "book was delete"})

        return self.dont_have_permission


class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response({"created": serializer.data})
