from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from http import HTTPStatus


from books.models import Book, Author, Genre
from books.serializers import (
    BookListSerializer,
    GenreSerializer,
    BookDetailSerializer,
    CreateBookSerializer,
)


class BookListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Book.objects.all()
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
        serializer = BookDetailSerializer(data=request.data, instance=book)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"update is good": serializer.data})

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return self.error_except

        if book.owner == request.user or request.user.is_superuser:
            book.delete()
            return Response({"well done": "book was delete"})
        return Response({"error": "You don't have permissions"})
