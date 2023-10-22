from django.db.models import Q
from django.shortcuts import render
from .forms import SearchForm
from django.views.generic import ListView, View
from .models import Book


class IndexView(ListView):
    template_name = "index.html"
    model = Book


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
