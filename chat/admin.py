from django.contrib import admin

from .models import PrivateMessage


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "timestamp"]
    fields = ["sender", "recipient", "message", "timestamp"]
    readonly_fields = ["timestamp"]
