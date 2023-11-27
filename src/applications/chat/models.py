from django.db import models

from src.applications.users.models import User


class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    message = models.CharField(max_length=350)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sender {self.sender} | recipient {self.recipient}"
