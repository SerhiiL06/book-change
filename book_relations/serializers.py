from rest_framework import serializers

from .models import BookRelations


class BookRelationsSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = BookRelations
        fields = ["book", "user", "bookmark", "rating"]

    def get_book(self, obj):
        return obj.book.title

    def get_user(self, obj):
        return obj.user.email
