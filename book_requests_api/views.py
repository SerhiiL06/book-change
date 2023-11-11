from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book_requests.models import BookRequest
from book_requests.serializers import BookRequestSerializer
from book_requests.tasks import send_notification_about_request
from books.models import Book
from users.decorators import is_object_owner


class BookRequestListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = BookRequest.objects.filter(
            Q(book__owner=request.user) | Q(request_from_user=request.user)
        )

        serializer = BookRequestSerializer(instance=queryset, many=True)

        return Response({"request list": serializer.data})

    def post(self, request):
        serializer = BookRequestSerializer(data=request.data)
        try:
            book = Book.objects.get(id=request.data["book_id"])
        except Book.DoesNotExist:
            return Response({"error": "book doesn't exists"})
        check_request = BookRequest.objects.filter(
            book_id=request.data["book_id"], request_from_user=request.user
        )

        if not check_request.first() and not is_object_owner(request.user, book.owner):
            serializer.is_valid(raise_exception=True)

            serializer.save(request_from_user_id=request.user.id)
            send_notification_about_request.delay(book.id)
            return Response({"OK": serializer.data})

        return Response("Requests already exists")
