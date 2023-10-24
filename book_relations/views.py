from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
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


def left_rating(request):
    if request.method == "POST":
        book_id = int(request.POST["book_id"])
        rating = int(request.POST["rating"])
        relation, created = BookRelations.objects.get_or_create(
            user=request.user, book_id=book_id
        )

        relation.rating = rating
        relation.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])
