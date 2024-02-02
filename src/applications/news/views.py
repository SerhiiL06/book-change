from typing import Any

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, View

from .forms import NewsForm
from .models import Like, News


@method_decorator(login_required, name="get")
class NewsListView(ListView):
    template_name = "news/news-list.html"
    model = News

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()

        return queryset.filter(publish=True)


class CreateNews(CreateView):
    template_name = "news/create-news.html"
    model = News
    form_class = NewsForm
    success_url = reverse_lazy("news:news-list")

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = NewsForm(request.POST)

        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect("news:news-list")


class DeleteNews(DeleteView):
    model = News
    template_name = "news/news-list.html"
    success_url = reverse_lazy("news:news-list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().post(request, *args, **kwargs)


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
