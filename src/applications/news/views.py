from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import HttpResponseRedirect, redirect, get_object_or_404
from django.views.generic import ListView, View

from .models import Like, News


class NewsListView(ListView):
    template_name = "news/news-list.html"
    model = News

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()

        return queryset.filter(publish=True)


class LikeView(View):
    def get_success_url(self):
        return redirect("news:news-list")

    def get(self, request, news_id):
        news = get_object_or_404(News, id=news_id)

        check_like, create = Like.objects.get_or_create(user=request.user, news=news)

        if create:
            news.likes += 1

        else:
            check_like.delete()

            news.likes -= 1

        news.save()

        return HttpResponseRedirect(request.META["HTTP_REFERER"])
