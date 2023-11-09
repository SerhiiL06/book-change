from rest_framework import serializers

from book_relations.models import BookRelations

from .models import Author, Book, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["title"]


class BookListSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "genre", "owner", "avg_rating"]

    def get_owner(self, obj):
        return obj.owner.full_name()

    def get_avg_rating(self, obj):
        rating = BookRelations.objects.get_rating(obj)
        return rating if rating else f"None rating"


class CreateBookSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    genre_id = serializers.IntegerField()
    author_id = serializers.IntegerField()
    owner_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Book.objects.create(**validated_data)


class BookDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "author",
            "genre",
            "owner",
            "created_at",
            "rating",
        ]

    def create(self, validated_data):
        new_book = Book.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            genre=validated_data["genre"],
            author=validated_data["author"],
        )
        return new_book

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

    def get_rating(self, obj):
        rating = BookRelations.objects.get_rating(obj)
        return rating
