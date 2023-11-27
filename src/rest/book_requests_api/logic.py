from django.db.models import Q
from rest_framework.response import Response

from src.applications.book_requests.models import BookRequest


def check_if_request_exists(request, request_id):
    try:
        book_request = BookRequest.objects.get(
            Q(id=request_id)
            & (Q(request_from_user=request.user) | Q(book__owner=request.user))
        )
    except BookRequest.DoesNotExist:
        return Response("book request doesnt exists")

    return book_request
