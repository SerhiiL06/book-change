from django.db.models import Q

from .models import BookRequest


def total_requests(request):
    user = request.user
    if user.is_authenticated:
        return {
            "total_requests": BookRequest.objects.filter(
                Q(request_from_user=user) | Q(book__owner=user)
            ).count()
        }

    return {"total_requests": 0}
