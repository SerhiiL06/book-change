from django.db.models import Avg
from django.urls import reverse

from .models import BookRelations


def check_bookmark(user, books):
    if user.is_authenticated:
        for book in list(books):
            relation = BookRelations.objects.filter(user=user, book=book).first()
            if relation:
                return relation.bookmark
    return False


def get_user_rating(user):
    rating = BookRelations.objects.filter(book__owner=user).aggregate(
        avg_user_rating=Avg("rating")
    )["avg_user_rating"]
    return round(rating, 2) if rating else 0


def generate_previous_message_for_share(request, slug):
    link_to_book = request.build_absolute_uri(
        reverse("books:detail-book", kwargs={"slug": slug})
    )

    message = f"Hey I wanted the new interesting book! Link here: {link_to_book}"

    return message
