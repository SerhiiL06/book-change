from django.contrib import admin

from .models import BookRelations


@admin.register(BookRelations)
class BookRealtionsAdmin(admin.ModelAdmin):
    list_display = ["book", "__str__"]
