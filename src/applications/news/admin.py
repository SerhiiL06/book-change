from collections import OrderedDict
from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest

from .models import Like, News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "publish"]
    readonly_fields = ["created_date", "likes"]
    actions = ["unpublish", "publish"]

    @admin.action(description="change to unpublish")
    def unpublish(modeladmin, request, queryset):
        queryset.update(publish=False)

    @admin.action(description="change to publish")
    def publish(modeladmin, request, queryset):
        queryset.update(publish=True)


admin.site.register(Like)
