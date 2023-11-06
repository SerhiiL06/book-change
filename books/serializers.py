from rest_framework import serializers

from book_relations.models import BookRelations

from .models import Author, Book, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["title"]


class BookListSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "genre", "owner", "avg_rating"]

    def get_owner(self, obj):
        return obj.owner.full_name()

    def get_genre(self, obj):
        return obj.genre.title

    def get_avg_rating(self, obj):
        rating = BookRelations.objects.get_rating(obj)
        return rating


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        exclude = ["slug", "rating", "last_update"]

    def get_description(self, obj):
        return f"{obj.description[:20]}..."

    def get_owner(self, obj):
        return obj.owner.full_name()

    def get_genre(self, obj):
        return obj.genre.title

    def get_created_at(self, obj):
        return obj.created_at.date()

    def get_author(self, obj):
        return obj.author.name

    def get_avg_rating(self, obj):
        rating = BookRelations.objects.get_rating(obj)
        return rating
