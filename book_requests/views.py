from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .forms import BookRequestForm

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
