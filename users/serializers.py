from rest_framework import serializers

from django.core.mail import send_mail
from django.conf import settings
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
    last_activity = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    profile = UserProfileSerializer(many=False, required=False)
    total_books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "last_activity",
            "email",
            "total_books",
            "followers",
            "profile",
        ]

    # methods

    def get_last_activity(self, obj):
        return obj.last_activity.date()

    def get_followers(self, obj):
        return obj.followers.count()

    def get_total_books(self, obj):
        return obj.my_books.count()


class UserDetailSerializer(serializers.ModelSerializer):
    last_activity = serializers.SerializerMethodField()
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
            "last_activity",
            "email",
            "total_books",
            "my_books",
            "followers",
            "profile",
        ]

    def get_last_activity(self, obj):
        return obj.last_activity.date()

    def get_join_at(self, obj):
        return obj.join_at.date()

    def get_followers(self, obj):
        return obj.followers.count()

    def get_total_books(self, obj):
        return obj.my_books.count()


class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
    to = serializers.EmailField()

    def save(self, **kwargs):
        message = kwargs.get("message")
        to_user = kwargs.get("to")
