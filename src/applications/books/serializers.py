from rest_framework import serializers

from src.applications.book_relations.models import BookRelations

from .models import Author, Book, Comment, Genre


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False)
    edited = serializers.DateTimeField(required=False)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["user", "book", "comment", "created_at", "edited"]

    def get_user(self, obj):
        return obj.user.full_name()


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
    comments = serializers.SerializerMethodField()

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
            "comments",
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
        return round(rating, 2)

    def get_comments(self, obj):
        comments = Comment.objects.filter(book=obj)
        return CommentSerializer(comments, many=True).data


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
        return rating if rating else f"None rating"


class GenreSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ["title", "books"]

    def get_books(self, obj):
        return obj.books.count()


class GenreDetailSerializer(serializers.ModelSerializer):
    books = BookListSerializer(many=True)

    class Meta:
        model = Genre
        fields = ["title", "books"]


class AuthorListSerializer(serializers.ModelSerializer):
    country = serializers.CharField(read_only=True)
    total_books = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Author
        fields = ["name", "country", "total_books"]

    def get_total_books(self, obj):
        return obj.books.count()
