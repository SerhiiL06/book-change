from rest_framework import serializers
from rest_framework.response import Response

from .models import BookRequest


class BookRequestSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    request_from_user_id = serializers.IntegerField(read_only=True)
    comment = serializers.CharField(max_length=100)
    status = serializers.CharField(default="send")
    created = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data, user=None):
        return BookRequest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.book_id = validated_data.get("book_id")
        instance.request_from_user_id = validated_data.get("request_from_user_id")
        instance.comment = validated_data.get("comment")
        return instance

    def get_created(self, obj):
        return obj.created.date()
