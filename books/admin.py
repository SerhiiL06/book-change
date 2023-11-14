from .inlines import CommentInline, BookPDFInline
from django.contrib import admin


from .models import Author, Book, BookInPDF, Comment, Genre


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
    list_display_links = ["title", "owner"]
    list_select_related = ["in_pdf"]

    fields = ["title", "genre", "owner", "slug"]
    readonly_fields = ["owner"]

    list_filter = ["owner", "genre", "author"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [CommentInline, BookPDFInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]


@admin.register(BookInPDF)
class BookInPDFAdmin(admin.ModelAdmin):
    pass
