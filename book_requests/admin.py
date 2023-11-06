from django.contrib import admin

from .models import BookRequest, HistoryRequests


@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ["__str__", "status"]


@admin.register(HistoryRequests)
class HistoryRequestAdmin(admin.ModelAdmin):
    list_display = ["create_at"]
