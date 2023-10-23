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
