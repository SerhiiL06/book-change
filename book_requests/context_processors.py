from .models import BookRequest
from django.db.models import Q


def total_requests(request):
    user = request.user
    return {
        "total_requests": BookRequest.objects.filter(
            Q(request_from_user=user) | Q(book__owner=user)
        ).count()
    }
