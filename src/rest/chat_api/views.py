from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from src.applications.chat.models import PrivateMessage
from src.applications.chat.serializers import (PrivateMessageSerializer,
                                               SendPrivateMessage)
from src.applications.users.models import User

from .paginators import MessagePaginator


class PrivateMessageViewSet(viewsets.GenericViewSet):
    """
    A viewset for handling private messages.

    Actions:
        - `message_with`: Retrieve the messages between the authenticated user and another user.
        - `send_message`: Send a private message.

    """

    queryset = PrivateMessage.objects.all()
    serializer_class = PrivateMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MessagePaginator

    @action(
        methods=["get"],
        detail=True,
        url_path="messages",
        url_name="list_of_correspondence",
    )
    def message_with(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["pk"])

        queryset = PrivateMessage.objects.filter(
            (Q(sender=request.user) | Q(recipient=request.user))
            & (Q(sender=user) | Q(recipient=user))
        ).order_by("-timestamp")

        serializer = PrivateMessageSerializer(instance=queryset, many=True)

        return Response({"correspondence": serializer.data})

    @swagger_auto_schema(method="post", request_body=SendPrivateMessage)
    @action(
        methods=["post"], detail=False, url_path="send-message", url_name="send-message"
    )
    def send_message(self, request):
        serializer = SendPrivateMessage(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(sender=request.user)

        return Response(status=200, data="Message was send")
