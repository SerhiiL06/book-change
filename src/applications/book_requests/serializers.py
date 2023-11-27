from rest_framework import serializers
from rest_framework.response import Response

from src.applications.books.models import Book

from .models import BookRequest


class BookRequestListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    book_id = serializers.SerializerMethodField()
    request_from_user_id = serializers.IntegerField(read_only=True)
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

    def get_book_id(self, obj):
        book = Book.objects.get(id=obj.book_id)
        return book.title


class BookRequestDetailSerializer(serializers.ModelSerializer):
    request_from_user = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = BookRequest
        fields = ["book", "request_from_user", "created", "comment", "status"]
