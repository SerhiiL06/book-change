from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .forms import BookRequestForm
from django.views.generic import View
from django.db.models import F
from books.models import Book
from .models import BookRequest
from django.contrib.auth.decorators import login_required


@login_required()
def send_book_request(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.owner == request.user:
        return redirect("books:index")

    form = BookRequestForm()
    if request.method == "POST":
        check_request = BookRequest.objects.filter(
            book=book, request_from_user=request.user
        )
        if check_request.first():
            return HttpResponseRedirect(request.META["HTTP_REFERER"])

        comment = request.POST.get("comment")

        book_request, _ = BookRequest.objects.get_or_create(
            book=book, request_from_user=request.user, comment=comment, status="send"
        )

        # Send mail
        book_request.send_notification_about_request()
        return HttpResponseRedirect(reverse("books:index"))

    return render(request, "book-requests/open-request.html", {"form": form})


class BookRequestsView(View):
    def get(self, request):
        user = self.request.user
        queryset = BookRequest.objects.all().select_related("book", "request_from_user")
        incomming_requests = queryset.filter(book__owner=user)
        outcomming_request = queryset.filter(request_from_user=user)

        context = {"incomming": incomming_requests, "outcomming": outcomming_request}

        return render(request, "book-requests/book-request-list.html", context)


class BookRequestDetailView(View):
    def get(self, request, request_id, *args, **kwargs):
        req = BookRequest.objects.select_related("book", "request_from_user").get(
            id=request_id
        )
        user = request.user

        print(request.GET)

        if user not in [req.request_from_user, req.book.owner]:
            return redirect("books:index")

        check_request = bool(req.book.owner != user)
        context = {"check_request": check_request, "object": req}

        if req.book.owner == user:
            BookRequest.objects.filter(id=request_id).update(status="open")
        return render(request, "book-requests/book-request-detail.html", context)


def get_book_request(request):
    book_request = BookRequest.objects.get(id=request.POST["request_id"])

    book_request.book.owner = book_request.request_from_user

    book_request.save()

    book_request.delete()

    return redirect("book_request:my_requests")
