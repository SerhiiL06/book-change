from rest_framework import serializers
from .models import PrivateMessage


class PrivateMessageSerializer(serializers.ModelSerializer):
    recipient = serializers.CharField(read_only=True)
    sender = serializers.CharField(read_only=True)
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = PrivateMessage
        fields = ["sender", "recipient", "message", "timestamp"]

    def create(self, validated_data, user_id=None):
        return PrivateMessage.objects.create(**validated_data)

    def get_timestamp(self, obj):
        return obj.timestamp.datetime()
