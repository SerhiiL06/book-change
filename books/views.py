from typing import Any
from django.db.models import Q
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from book_relations.logic import check_bookmark
from book_relations.models import BookRelations
from .models import Book


class IndexView(ListView):
    template_name = "index.html"
    model = Book
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().select_related("owner").select_related("genre")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["check_bookmark"] = check_bookmark(
            user=self.request.user, books=self.get_queryset()
        )
        return context


class SearchView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "books/search.html")

    def post(self, request, *args, **kwargs):
        value = request.POST.get("searched").lower()

        books = Book.objects.filter(
            Q(title__icontains=value)
            | Q(genre__title__icontains=value)
            | Q(author__name=value)
        )
        if len(value) < 3:
            books = None
        return render(
            request, "books/search.html", {"object_list": books, "result": value}
        )


class DetailBookView(DetailView):
    template_name = "books/book-detail.html"
    queryset = Book.objects.all().select_related("genre").select_related("owner")
    cache_timeout = 60

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        cache_key = f"book_detail_{obj.id}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            context.update(cached_data)
        else:
            # average rating book
            context["avg"] = BookRelations.objects.get_rating(book=obj)
            # generate 3 random book
            context["recommended"] = Book.objects.get_recommended(obj.genre)
            # last 3 books
            context["last_books"] = self.get_queryset()[:3]

            cache.set(cache_key, context, self.cache_timeout)

        return context
