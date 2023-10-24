from django.db.models import Q

from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from book_relations.logic import check_bookmark
from book_relations.models import BookRelations
from .models import Book


class IndexView(ListView):
    template_name = "index.html"
    model = Book
    paginate_by = 8

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
    model = Book

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context["avg"] = BookRelations.objects.get_rating(book=obj)
        context["recommended"] = Book.objects.get_recommended(genre=obj.genre)
        context["last_books"] = (
            Book.objects.all()
            .order_by("-created_at")
            .values("slug", "title", "owner__first_name", "owner__id", "created_at")
        )[:3]

        return context
