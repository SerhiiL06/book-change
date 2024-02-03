from http import HTTPStatus

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from src.applications.book_relations.models import BookRelations
from src.applications.book_relations.serializers import (
    BookRelationsSerializer, CreateBookRelationSerializer, ShareBookSerializer)
from src.applications.books.models import Book
from src.applications.chat.models import PrivateMessage
from src.applications.users.models import User, UserFollowing
from src.applications.users.serializers import UserSerializer


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


class BookRelationsDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookRelations.objects.all()
    serializer_class = BookRelationsSerializer

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


class ShareBookAPIView(viewsets.GenericViewSet):
    http_method_names = ["get", "post"]
    permission_classes = [permissions.IsAuthenticated]
    queryset = PrivateMessage.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return super().get_serializer_class()
        return ShareBookSerializer

    @action(methods=["get"], detail=False)
    def get_friends_list(self, request, *args, **kwargs):
        ids = UserFollowing.objects.values_list("user_id").filter(
            followers_id=request.user.id
        )
        queryset = User.objects.filter(id__in=ids)

        serializer = UserSerializer(instance=queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=["post"], detail=False)
    def share_message(self, request, *args, **kwargs):
        data = ShareBookSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        data.save(sender=request.user)

        return Response({"message": "create"}, status.HTTP_201_CREATED)
