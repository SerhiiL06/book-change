from rest_framework import serializers

from .models import Genre, Author, Book


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["title"]


class BookSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Book
        exclude = ["slug", "rating", "last_update", "author"]

    def get_description(self, obj):
        return f"{obj.description[:20]}..."

    def get_owner(self, obj):
        return obj.owner.full_name()

    def get_genre(self, obj):
        return obj.genre.title

    def get_created_at(self, obj):
        return obj.created_at.date()
