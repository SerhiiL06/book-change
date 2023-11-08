from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from books.models import Book
from users.models import User


@shared_task()
def send_notification_about_request(book_id):
    book = Book.objects.get(id=book_id)
    subject = f"Hey your book {book} want user. Check site"
    message = f"Now one of the user want to get your book"
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[book.owner.email],
        fail_silently=True,
    )


@shared_task()
def send_email_about_success_request(user_id, book):
    user = User.objects.get(id=user_id)
    subject = f"Alarm, your request was success!"
    message = f"{book} is your! :)"
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=True,
    )
