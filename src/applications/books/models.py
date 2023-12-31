import random

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

from src.applications.users.models import User


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
    title = models.CharField(max_length=250, unique=True)
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
    genre = models.ForeignKey(
        Genre, on_delete=models.PROTECT, null=True, related_name="genre_books"
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_books")

    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = "/book_img/default-book-img.jpeg"
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_recommended(self, genre):
        recommend_ids = list(
            Book.objects.filter(genre=genre).values_list("id", flat=True)
        )

        list_book = random.sample(recommend_ids, len(recommend_ids))

        return Book.objects.filter(id__in=list_book[:3]).select_related("owner")

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

    def __str__(self):
        return f"{self.user.email} add comment to {self.book.title}"


class BookInPDF(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name="in_pdf")

    pdf = models.FileField(
        upload_to="book_in_pdf/", validators=[FileExtensionValidator(["pdf"])]
    )

    class Meta:
        verbose_name_plural = "Books_in_pdf"

    def __str__(self):
        return self.book.title
