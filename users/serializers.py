from rest_framework import serializers

from books.models import Book

from .models import User, UserProfile


class MyBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "phone_number", "country"]


class UserSerializer(serializers.ModelSerializer):
    join_at = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    my_books = MyBooksSerializer(many=True, required=False)
    profile = UserProfileSerializer(many=False, required=False)
    total_books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "join_at",
            "email",
            "total_books",
            "my_books",
            "followers",
            "profile",
        ]

    def get_join_at(self, obj):
        return obj.join_at.date()

    def get_followers(self, obj):
        return obj.followers.count()

    def get_total_books(self, obj):
        return obj.my_books.count()
