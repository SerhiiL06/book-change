from django.shortcuts import render, HttpResponseRedirect
from django.db.models import Q
from .models import PrivateMessage
from users.models import User


def chat_view(request, recipient):
    user = User.objects.get(id=recipient)
    messages = PrivateMessage.objects.filter(
        Q(sender=request.user, recipient=user) | Q(sender=user, recipient=request.user)
    ).select_related("sender", "recipient")
    return render(request, "chat/chat.html", {"messages": messages, "recipient": user})
