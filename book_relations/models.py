from django.db import models
from users.models import User
from books.models import Book


class BookRelationsManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.annotate()
        return queryset.filter(models.Q(bookmark=True) | models.Q(rating__gt=0))

    def get_rating(self, book):
        rating = (
            self.get_queryset()
            .filter(book=book)
            .aggregate(avg_rating=models.Avg("rating"))["avg_rating"]
        )
        return rating if rating else 0


class BookRelations(models.Model):
    RATING_CHOISES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_relation"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rait")

    bookmark = models.BooleanField(default=False)
    rating = models.SmallIntegerField(choices=RATING_CHOISES, blank=True, null=True)

    objects = BookRelationsManager()

    def __str__(self) -> str:
        if not self.rating:
            return f"{self.user.first_name} add to bookmark {self.book.title}"

        else:
            return f"{self.user.first_name} left a rating {self.rating}"
