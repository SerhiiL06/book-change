from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book_requests.models import BookRequest
from book_requests.serializers import (BookRequestDetailSerializer,
                                       BookRequestListSerializer)
from book_requests.tasks import (send_email_about_success_request,
                                 send_notification_about_request)
from books.models import Book
from users.decorators import is_object_owner

from .logic import check_if_request_exists


class BookRequestListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = BookRequest.objects.filter(
            Q(book__owner=request.user) | Q(request_from_user=request.user)
        )

        serializer = BookRequestListSerializer(instance=queryset, many=True)

        return Response({"request list": serializer.data})

    def post(self, request):
        serializer = BookRequestListSerializer(data=request.data)
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


class BookRequestDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):
        book_request = check_if_request_exists(request, request_id)

        if request.user != book_request.request_from_user:
            book_request.status = "open"
            book_request.save()

        serializer = BookRequestDetailSerializer(instance=book_request, many=False)

        return Response({"detail request": serializer.data})

    def post(self, request, request_id):
        book_request = check_if_request_exists(request, request_id)
        try:
            answer = request.data.get("answer")
        except ValueError:
            Response("enter the anwser please", status=404)

        if not request.data["answer"].lower() in ("ok", "failed"):
            return Response({"You may send ok or failed answer"})

        if answer.lower() == "ok":
            if request.user != book_request.request_from_user:
                book_request.de_json("success")

                # change owner for book
                book = Book.objects.get(id=book_request.book.id)
                book.owner = book_request.request_from_user
                book.save()

                send_email_about_success_request.delay(
                    book=book.title, user_id=book_request.request_from_user.id
                )

                book_request.delete()

                return Response({"OK": "Request success apply"})
            else:
                return Response({"you cannot apply your request"})

        book_request.de_json("failed")
        book_request.delete()

        return Response({"book request was failed"})
