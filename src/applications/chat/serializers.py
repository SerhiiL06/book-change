from django.utils import timezone
from rest_framework import serializers

from .models import PrivateMessage


class PrivateMessageSerializer(serializers.ModelSerializer):
    recipient = serializers.CharField(read_only=True)
    sender = serializers.CharField(read_only=True)

    class Meta:
        model = PrivateMessage
        fields = ["sender", "recipient", "message", "timestamp"]


class SendPrivateMessage(serializers.ModelSerializer):
    timestamp = serializers.HiddenField(default=timezone.now)

    class Meta:
        model = PrivateMessage
        fields = ["message", "recipient", "timestamp"]

    def create(self, validated_data):
        return PrivateMessage.objects.create(**validated_data)
