from django.contrib import admin

from .models import BookRelations


@admin.register(BookRelations)
class BookRealtionsAdmin(admin.ModelAdmin):
    list_display = ["book", "__str__"]
    fields = ["book", "user", "bookmark", "rating"]
    readonly_fields = fields
    list_filter = ["rating", "bookmark"]
