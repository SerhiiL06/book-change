from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import News


class NewsListView(ListView):
    template_name = "news/news-list.html"
    model = News

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()

        return queryset.filter(publish=True)
