from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def user_loggin(sender, user, **kwargs):
    user.status = "online"
    user.save()


@receiver(user_logged_out)
def user_logout(sender, user, **kwargs):
    user.status = "offline"
    user.save()
