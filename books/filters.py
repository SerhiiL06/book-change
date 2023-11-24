from django.contrib import admin
from django.db.models.functions import Length
from django.db.models import Avg
from .models import Book
from typing import Any


class TextFilter(admin.SimpleListFilter):
    title = "description length"
    parameter_name = "text"

    def lookups(self, request: Any, model_admin: Any):
        values = (("short", "Short text"), ("long", "Long text"))

        return values

    def queryset(self, request, queryset):
        if self.value() == "short":
            return Book.objects.annotate(descr_len=Length("description")).filter(
                descr_len__lt=600
            )

        if self.value() == "long":
            return Book.objects.annotate(descr_len=Length("description")).filter(
                descr_len__gte=600
            )
