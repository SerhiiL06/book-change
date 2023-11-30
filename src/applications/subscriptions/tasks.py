from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings


@shared_task()
def send_email_about_payment(session):
    time = datetime.utcfromtimestamp(session.created)
    subject = f"You are have success payment for {session.amount_total / 100}"
    message = f"Your operation at {time} well done"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = session.customer_details.email
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[recipient_list],
        fail_silently=True,
    )
