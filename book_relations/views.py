from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from .models import BookRelations
from books.models import Book


def add_to_bookmark(request, book_slug):
    book = Book.objects.get(slug=book_slug)
    relation, created = BookRelations.objects.get_or_create(
        user=request.user, book=book
    )
    relation.bookmark = not relation.bookmark
    relation.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
