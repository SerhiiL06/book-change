from django.contrib import admin
from .models import Genre, Author, Book, Comment, BookInPDF


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "genre", "owner"]
    list_filter = ["genre", "owner"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]


@admin.register(BookInPDF)
class BookInPDFAdmin(admin.ModelAdmin):
    pass
