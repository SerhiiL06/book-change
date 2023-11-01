from django.db import models
from books.models import Book
from users.models import User
from django.core.mail import send_mail


class BookRequest(models.Model):
    STATUSES = (
        ("send", "send"),
        ("open", "open"),
        ("fail", "failed"),
        ("comp", "complete"),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_from_user = models.ForeignKey(User, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    comment = models.CharField(max_length=100, null=True)

    status = models.CharField(choices=STATUSES, max_length=4)

    def __str__(self) -> str:
        return f"Requst from {self.request_from_user} to book '{self.book.title}'"

    def send_notification_about_request(self):
        subject = f"Hey your book {self.book} want user. Check site"
        message = f"Now one of the user want to get your book"
        send_mail(
            subject=subject,
            message=message,
            from_email=self.request_from_user.email,
            recipient_list=[self.book.owner.email],
            fail_silently=True,
        )


# class HistoryRequest(models.Model):

#     book_request = models.JSONField()
