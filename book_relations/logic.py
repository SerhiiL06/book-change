from django.db.models import Avg

from .models import BookRelations


def check_bookmark(user, books):
    if not user.is_authenticated:
        return False
    for book in list(books):
        relation = BookRelations.objects.filter(user=user, book=book)
        if not relation.first():
            return False
        else:
            return relation.first().bookmark


def get_user_rating(user):
    rating = BookRelations.objects.filter(book__owner=user).aggregate(
        avg_user_rating=Avg("rating")
    )["avg_user_rating"]
    return round(rating, 2) if rating else 0
