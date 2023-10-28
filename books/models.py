from django.db import models
import random

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


class BookManager(models.Manager):
    def get_recommended(self, genre):
        recommend_books = list(Book.objects.filter(genre=genre).select_related("owner"))
        if len(recommend_books) < 3:
            recommend_books += list(self.get_queryset())[:4]
        return random.sample(recommend_books, 3)


class Book(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(default="")
    description = models.TextField(blank=True, null=True)
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

    objects = BookManager()

    def save(self, *args, **kwargs):
        if not self.rating:
            self.rating = 0
        if not self.image:
            self.image = "/book_img/default-book-img.jpeg"
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
