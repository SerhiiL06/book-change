from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from src.applications.books.models import Book

from .models import BookRelations


def add_to_bookmark(request, book_slug):
    """Add book in bookmark"""
    book = Book.objects.get(slug=book_slug)
    relation, _ = BookRelations.objects.get_or_create(user=request.user, book=book)
    relation.bookmark = not relation.bookmark
    relation.save()
    return HttpResponseRedirect(reverse("books:index"))


def left_rating(request):
    """User left rating"""
    if request.method == "POST":
        book_id = int(request.POST["book_id"])
        rating = int(request.POST["rating"])
        relation, _ = BookRelations.objects.get_or_create(
            user=request.user, book_id=book_id
        )

        relation.rating = rating
        relation.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def bookmark_list(request):
    """User bookmark list"""
    obj_list = BookRelations.objects.filter(
        Q(user=request.user) & Q(bookmark=True)
    ).select_related("book")
    context = {"object_list": obj_list}
    return render(request, "book-relations/bookmark-list.html", context)
