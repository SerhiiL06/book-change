from typing import Any

from django.db.models.query import QuerySet
from django.db.models.functions import Length
from .inlines import CommentInline, BookPDFInline, BookInline
from django.contrib import admin


from .models import Author, Book, BookInPDF, Comment, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    inlines = [BookInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


class TextFilter(admin.SimpleListFilter):
    title = "description length"
    parameter_name = "text"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        values = (("short", "Short text"), ("long", "Long text"))

        return values

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == "short":
            return Book.objects.annotate(descr_len=Length("description")).filter(
                descr_len__lt=600
            )

        if self.value() == "long":
            return Book.objects.annotate(descr_len=Length("description")).filter(
                descr_len__gte=600
            )


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
