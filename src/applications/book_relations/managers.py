from django.db import models


class BookRelationsManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(models.Q(bookmark=True) | models.Q(rating__gt=0))

    def get_rating(self, book):
        rating = (
            self.get_queryset()
            .filter(book=book)
            .aggregate(avg_rating=models.Avg("rating"))["avg_rating"]
        )
        return rating if rating else 0
