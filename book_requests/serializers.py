from rest_framework import serializers
from .models import BookRequest


class BookRequestSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    request_from_user_id = serializers.IntegerField()
    comment = serializers.CharField(max_length=100)
    status = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return BookRequest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.book_id = validated_data.get("book_id")
        instance.request_from_user_id = validated_data.get("request_from_user_id")
        instance.comment = validated_data.get("comment")
        return instance
