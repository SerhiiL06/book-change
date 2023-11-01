from django.contrib import admin
from .models import BookRequest


@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ["__str__", "status"]


# Register your models here.
