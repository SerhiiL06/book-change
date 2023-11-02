from django.db import models
from books.models import Book
from users.models import User
from django.core.mail import send_mail
from django.utils import timezone
from base.settings import EMAIL_HOST_USER


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

    def send_email_about_success_request(self):
        subject = f"Alarm, your request was success!"
        message = f"{self.book} is your! :)"
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.request_from_user.email],
            fail_silently=True,
        )

    def de_json(self, status):
        data = {
            "book": self.book.title,
            "from": self.request_from_user.full_name(),
            "to": self.book.owner.full_name(),
            "status": status,
            "opetation_date": str(timezone.now().date()),
        }
        HistoryRequests.objects.create(data=data)


class HistoryRequests(models.Model):
    data = models.JSONField(default=dict)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "History Requests"

    def __str__(self) -> str:
        return self.data["book"]
