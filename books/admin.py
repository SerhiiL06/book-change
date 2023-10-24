from django.contrib import admin
from .models import Genre, Author, Book


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "genre", "image"]
    prepopulated_fields = {"slug": ["title"]}
