from rest_framework import serializers

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
