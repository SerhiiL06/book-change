from typing import Any
from django.db.models import Q
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView, CreateView
from book_relations.logic import check_bookmark
from book_relations.models import BookRelations
from .forms import CreateBookForm
from .models import Book, Comment


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


class DetailBookView(DetailView):
    template_name = "books/book-detail.html"
    queryset = Book.objects.all().select_related("genre", "owner")

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)

        # average rating book
        context["avg"] = BookRelations.objects.get_rating(book=obj)
        # generate 3 random book
        context["recommended"] = obj.get_recommended(obj.genre)
        # last 3 books
        context["last_books"] = self.get_queryset()[:3]

        context["comments"] = (
            Comment.objects.filter(book=self.get_object())
            .select_related("user")
            .order_by("-created_at")
        )

        return context

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(slug=kwargs["slug"])
        Comment.objects.create(
            user=self.request.user, book=book, comment=request.POST["message"]
        )
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class CreateBookView(CreateView):
    template_name = "books/create-book.html"
    model = Book
    form_class = CreateBookForm
    success_url = reverse_lazy("books:index")

    def post(self, request):
        form = CreateBookForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            form.save_m2m()

            return redirect("books:index")

        return HttpResponseRedirect(request.META["HTTP_REFERER"])


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
