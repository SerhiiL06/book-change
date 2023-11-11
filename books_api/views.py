from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from http import HTTPStatus


from books.models import Book, Author, Genre, Comment
from books.serializers import (
    BookListSerializer,
    GenreSerializer,
    AuthorListSerializer,
    GenreDetailSerializer,
    BookDetailSerializer,
    CreateBookSerializer,
    CommentSerializer,
)


class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response({"created": serializer.data})


class AuthorListAPIView(APIView):
    def get(self, request):
        queryset = Author.objects.all()
        serializer = AuthorListSerializer(queryset, many=True)
        return Response({"author_list": serializer.data})

    def post(self, request):
        new_author = AuthorListSerializer(data=request.data)
        new_author.is_valid(raise_exception=True)
        new_author.save(country="Spanish")
        return Response({"author create": new_author.data})


class AuthorDetailAPIView(APIView):
    author_doesnt_exists = ValueError("This author was dont exists")
    dont_have_permission = Response({"error": "you dont have permission"})

    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            raise self.author_doesnt_exists

        serializer = AuthorListSerializer(author, many=False)

        return Response({"author": serializer.data})

    def patch(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            raise self.author_doesnt_exists

        if request.user.is_staff:
            serializer = AuthorListSerializer(instance=author, data=request.data)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response({"update": serializer.data})

        return self.dont_have_permission

    def delete(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            raise self.author_doesnt_exists

        if request.user.is_superuser:
            author.delete()

            return Response({"well done author delete"})

        return self.dont_have_permission


class GenreListAPIView(APIView):
    def get(self, request):
        queryset = Genre.objects.all()
        serializer = GenreSerializer(instance=queryset, many=True)
        return Response({"genre_list": serializer.data})

    def post(self, request):
        genre = GenreSerializer(data=request.data)

        genre.is_valid(raise_exception=True)

        genre.save()

        return Response({"well done": "create"})


class GenreDetailAPIView(APIView):
    def get(self, request, genre_id):
        try:
            genre = Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist:
            return Response({"Genre doesn't exists"})

        serializer = GenreDetailSerializer(instance=genre, many=False)

        return Response({"genre": serializer.data})

    def patch(self, request, genre_id):
        try:
            genre = Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist:
            return Response({"Genre doesn't exists"})

        serializer = GenreDetailSerializer(instance=genre, data=request.data)

        serializer.is_valid()

        serializer.save()

        return Response({"Update was good!"})


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
