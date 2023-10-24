from django.db import models

from users.models import User
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.utils.text import slugify


class Genre(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=250)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(default="")
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(
        validators=[MaxValueValidator(5)], max_digits=3, decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to="book_img/",
        validators=[FileExtensionValidator(["jpg", "JPEG"])],
        null=True,
        blank=True,
    )
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_books")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# class BookRelations(models.Model):
#     RAITING = (
#         (1, 1),
#         (2, 2),
#         (3, 3),
#         (4, 4),
#         (5, 5),
#     )

#     book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="relation")
#     raiting = models.SmallIntegerField(choices=RAITING)
#     in_request = models.BooleanField(default=False)
#     client = models.ForeignKey(
#         to=User, on_delete=models.CASCADE, related_name="active_book"
#     )


# class RequestBook(models.Model):


#     book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
#     customer = models.ForeignKey(
#         to=User, on_delete=models.CASCADE, related_name="requests"
#     )
#     status = models.CharField()
