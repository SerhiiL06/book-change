from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.applications.book_relations.models import BookRelations
from django.utils import timezone


from .models import Author, Book, Comment, Genre


class LatestBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "created_at", "owner"]


class RecommendedSerializer(LatestBooksSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment", "book"]

    def validate_comment(self, value):
        if not len(value) in range(10, 100):
            raise ValidationError(detail="Your comment is short or so long")

        return value

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class UpdateCommentSerializer(CommentSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ["id", "comment"]

    def update(self, instance, validated_data):
        if instance.user != validated_data["current_user"]:
            raise ValidationError("You cannot update this comment")

        instance.comment = validated_data["comment"]

        instance.save()

        return instance


class CreateBookSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    created_at = serializers.HiddenField(default=timezone.now)

    class Meta:
        model = Book
        fields = [
            "title",
            "image",
            "description",
            "genre",
            "author",
            "created_at",
        ]

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
    comments = CommentSerializer(many=True)

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

    def to_representation(self, instance):
        latest_books_queryset = Book.objects.all()[:3]

        latest_books_data = LatestBooksSerializer(
            instance=latest_books_queryset, many=True
        ).data

        recommended_queryset = instance.get_recommended(genre=instance.genre)

        recommended_data = RecommendedSerializer(
            instance=recommended_queryset, many=True
        ).data

        representation = super().to_representation(instance)
        representation["latest_books"] = latest_books_data
        representation["recommended"] = recommended_data
        return representation


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


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "description", "image"]


# Genre serializers


class GenreListSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ["title", "books"]

    def get_books(self, obj):
        return obj.genre_books.count()


class GenreDetailSerializer(GenreListSerializer):
    genre_books = BookDetailSerializer(many=True)

    class Meta:
        model = Genre
        fields = GenreListSerializer.Meta.fields + ["genre_books"]


# Authors serializers
class AuthorListSerializer(serializers.ModelSerializer):
    country = serializers.CharField(read_only=True)
    total_books = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "country", "total_books"]

    def get_total_books(self, obj):
        return obj.books.count()


class AuthorDetailSerializer(AuthorListSerializer):
    from src.applications.books.serializers import BookListSerializer

    books = BookListSerializer(many=True)

    class Meta:
        model = Author
        fields = AuthorListSerializer.Meta.fields + ["books"]
