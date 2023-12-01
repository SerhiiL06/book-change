from django.db import models

from src.applications.books.models import Book
from src.applications.users.models import User
from .managers import BookRelationsManager


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

    class Meta:
        verbose_name_plural = "Book relations"
