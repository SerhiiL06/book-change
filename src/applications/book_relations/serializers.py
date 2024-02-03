from rest_framework import serializers
from rest_framework.response import Response

from src.applications.chat.models import PrivateMessage
from src.applications.users.models import User

from .models import BookRelations


class BookRelationsSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BookRelations
        fields = ["book", "user", "bookmark", "rating"]

    def get_book(self, obj):
        return obj.book.title

    def get_user(self, obj):
        return obj.user.full_name()


class CreateBookRelationSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()
    bookmark = serializers.BooleanField(required=False)
    rating = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        if "bookmark" in validated_data:
            instance.bookmark = validated_data.get("bookmark")
        if "rating" in validated_data:
            instance.rating = validated_data.get("rating")
        instance.save()
        return instance


class ShareBookSerializer(serializers.Serializer):
    message = serializers.CharField()
    recipient = serializers.IntegerField()

    def create(self, validated_data):

        recipient = User.objects.filter(id=validated_data["recipient"])

        if not recipient.first():
            raise Response({"message": "user with this id doesnt exists"})

        msg = PrivateMessage.objects.create(
            message=validated_data["message"],
            recipient=recipient.first(),
            sender=validated_data["sender"],
        )

        return msg
