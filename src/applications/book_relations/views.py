from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from src.applications.books.models import Book
from src.applications.chat.forms import ShareMessageForm
from src.applications.chat.models import PrivateMessage
from src.applications.users.models import User

from .logic import generate_previous_message_for_share
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


@method_decorator(login_required, "get")
class ShareMessageView(View):
    template_name = "book-relations/share-book.html"
    model = PrivateMessage

    def get(self, request, *args, **kwargs):
        book = kwargs.get("book_slug")
        message = generate_previous_message_for_share(request, book)

        form = ShareMessageForm(data={"message": message}, user=request.user.id)

        context = {"form": form, "book": book}
        return render(request, "book-relations/share-book.html", context=context)

    def post(self, request, *args, **kwargs):
        if not request.POST.get("recipient"):
            messages.error(request, "Recipient field is requeired")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        book = kwargs.get("book_slug")

        recipient = User.objects.get(id=request.POST.get("recipient"))

        new_message = PrivateMessage(
            sender=request.user,
            recipient=recipient,
            message=request.POST.get("message"),
        )

        new_message.save()

        messages.info(request, "Message was sent")

        return HttpResponseRedirect(reverse("books:detail-book", kwargs={"slug": book}))
