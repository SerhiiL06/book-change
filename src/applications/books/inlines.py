from .models import Comment, BookInPDF, Book
from django.contrib import admin


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ["comment"]
    readonly_fields = ["comment"]
    max_num = 2
    extra = 1


class BookPDFInline(admin.TabularInline):
    model = BookInPDF
    extra = 0


class BookInline(admin.TabularInline):
    model = Book
    fields = ["title", "image"]
    extra = 1
