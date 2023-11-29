from typing import Any

from django.contrib import admin
from django.db.models.functions import Length

from .filters import TextFilter
from .inlines import BookInline, BookPDFInline, CommentInline
from .models import Author, Book, BookInPDF, Comment, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    inlines = [BookInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "genre", "owner"]

    list_display_links = ["title", "owner"]
    list_select_related = ["in_pdf"]

    fields = ["title", "genre", "owner", "slug"]
    readonly_fields = ["owner"]

    list_filter = ["owner", "genre", "author", TextFilter]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [CommentInline, BookPDFInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]


@admin.register(BookInPDF)
class BookInPDFAdmin(admin.ModelAdmin):
    pass
