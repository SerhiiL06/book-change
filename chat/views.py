from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import View

from users.models import User

from .models import PrivateMessage


class ChatView(View):
    def get(self, request, recipient, *args, **kwargs):
        user = User.objects.get(id=recipient)
        messages = PrivateMessage.objects.filter(
            Q(sender=request.user, recipient=user)
            | Q(sender=user, recipient=request.user)
        ).select_related("sender", "recipient")

        contact_list = (
            PrivateMessage.objects.filter(
                Q(sender=request.user) | Q(recipient=request.user)
            )
            .select_related("recipient", "sender")
            .distinct("sender")
        )

        context = {
            "messages": messages,
            "recipient": user,
            "contact_list": contact_list,
        }
        return render(request, "chat/chat.html", context)

    def post(self, request, *args, **kwargs):
        sender = request.user
        recipient = request.POST["recipient"]
        user = User.objects.get(id=recipient)
        message = request.POST["message"]
        PrivateMessage.objects.create(sender=sender, recipient=user, message=message)
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
