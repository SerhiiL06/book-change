from django.db.models import Q
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import PrivateMessage
from chat.serializers import PrivateMessageSerializer
from users.models import User


class PrivateMessageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("user not exist")
        queryset = PrivateMessage.objects.filter(
            (Q(sender=request.user) | Q(recipient=request.user))
            & (Q(sender=user) | Q(recipient=user))
        ).order_by("-timestamp")
        serializer = PrivateMessageSerializer(instance=queryset, many=True)

        return Response({"messages": serializer.data})

    def post(self, request, user_id):
        message = PrivateMessageSerializer(data=request.data)
        message.is_valid(raise_exception=True)
        user = User.objects.get(id=user_id)
        message.save(sender=request.user, recipient=user)
        return Response("message was sent")
