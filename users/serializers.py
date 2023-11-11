from rest_framework import serializers

from rest_framework.response import Response
from django.conf import settings
from books.models import Book

from .models import User, UserProfile, UserFollowing


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


class UserFollowingSerializer(serializers.ModelSerializer):
    # user_id = serializers.SerializerMethodField()
    followers_id = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ["user_id", "followers_id"]

    def create(self, validated_data):
        user, create = UserFollowing.objects.get_or_create(
            user_id=validated_data["user_id"],
            followers_id=validated_data["followers_id"],
        )
        if not create:
            user.delete()
            return Response(status=202)

        return user

    def get_user_id(self, obj):
        return obj.user_id.full_name()

    def get_followers_id(self, obj):
        return obj.followers_id.full_name()


class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
    to = serializers.EmailField()

    def save(self, **kwargs):
        message = kwargs.get("message")
        to_user = kwargs.get("to")
