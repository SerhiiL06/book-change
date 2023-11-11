from http import HTTPStatus

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from book_relations.models import BookRelations
from book_relations.serializers import (BookRelationsSerializer,
                                        CreateBookRelationSerializer)
from books.models import Book


class BookRelationsAPIView(APIView):
    def get(self, request):
        queryset = BookRelations.objects.all()
        user_search = request.query_params.get("user_id")
        book_search = request.query_params.get("book")
        ordering_search = request.query_params.get("ordering")

        if user_search:
            queryset = queryset.filter(user_id=user_search)
        if book_search:
            queryset = queryset.filter(book__title__icontains=book_search)
        if ordering_search:
            queryset = queryset.order_by(ordering_search)
        serializer = BookRelationsSerializer(queryset, many=True)
        return Response({"book_relations": serializer.data})

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"Login please"})

        serializer = CreateBookRelationSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        book = Book.objects.get(id=serializer.validated_data["book_id"])
        book_rel, create = BookRelations.objects.get_or_create(
            book=book, user=request.user
        )
        if create:
            serializer.save(user=request.user)

        else:
            serializer.update(
                instance=book_rel, validated_data=serializer.validated_data
            )

        return Response({"OK"})


class BookRelationsDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"book doesnt exists"})

        try:
            relation = BookRelations.objects.get(user=request.user, book=book)
        except BookRelations.DoesNotExist:
            return Response({"relations doesn't exists"}, status=HTTPStatus.BAD_REQUEST)

        serializer = BookRelationsSerializer(relation, many=False)

        return Response({"relations_info": serializer.data})

    def patch(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"book doesnt exists"})

        try:
            relation = BookRelations.objects.get(user=request.user, book=book)
        except BookRelations.DoesNotExist:
            return Response({"relations doesn't exists"}, status=HTTPStatus.BAD_REQUEST)

        serializer = BookRelationsSerializer(data=request.data, instance=relation)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"object was updated"})


class UserBookmarkListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = BookRelations.objects.filter(user=request.user, bookmark=True)
        serializer = BookRelationsSerializer(instance=queryset, many=True)
        return Response({"bookmark_list": serializer.data})
