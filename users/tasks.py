from celery import shared_task
from django.core.mail import send_mail
from django_email_verification import send_email

from base.settings import EMAIL_HOST_USER

from .models import User


@shared_task()
def send_email_verification(user_id):
    user = User.objects.get(pk=user_id)
    send_email(user)


@shared_task()
def send_message(subject, message, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
    )


@shared_task()
def send_news_email():
    users = User.objects.filter(news_letter__news_mailer=True)
    for u in users:
        send_mail(
            subject="It's can be interesting for you",
            message="Hello",
            from_email=EMAIL_HOST_USER,
            recipient_list=[u.email],
            fail_silently=False,
        )

    print(f"{len(users)} message will be sent")
