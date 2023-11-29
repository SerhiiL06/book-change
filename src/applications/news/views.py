from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import Resolver404
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
        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            raise Resolver404()

        check_like = Like.objects.filter(user=request.user, news=news)

        if not check_like.first():
            like = Like(news=news, user=request.user)

            like.save()

            news.likes += 1

            news.save()

            return HttpResponseRedirect(request.META["HTTP_REFERER"])

        check_like.first().delete()

        news.likes -= 1

        news.save()

        return HttpResponseRedirect(request.META["HTTP_REFERER"])
