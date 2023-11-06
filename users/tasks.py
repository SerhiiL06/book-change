from celery import shared_task
from .models import User
from django.core.mail import send_mail
from django_email_verification import send_email


@shared_task()
def send_email_verification(user):
    send_email(user)


@shared_task()
def send_message(subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email="sergiy06061997@gmail.com",
        recipient_list=["sergiy06061997@gmail.com"],
        fail_silently=True,
    )
