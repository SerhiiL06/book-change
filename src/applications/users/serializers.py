from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from src.applications.books.models import Book

from .models import User, UserEmailNewsLetter, UserFollowing, UserProfile


class MyBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name"]
        abstract = True


class UserListSerializer(UserSerializer):
    total_books = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ["total_books", "followers"]

    def get_total_books(self, obj):
        return obj.my_books.count()

    def get_followers(self, obj):
        return obj.followers.count()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone_number", "country", "social_link", "profession"]


class UserDetailSerializer(UserSerializer):
    my_books = MyBooksSerializer(many=True)
    avatar = serializers.ImageField(source="image")
    profile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + [
            "about",
            "avatar",
            "status",
            "is_staff",
            "is_active",
            "my_books",
            "profile",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "image", "about", "profile"]


class FollowersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ["user_id", "followers_id"]


class FollowingSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        if validated_data["user_id"] == validated_data["followers_id"]:
            raise ValidationError(detail="You cannot subs youself")
        user, create = UserFollowing.objects.get_or_create(
            user_id=validated_data["user_id"],
            followers_id=validated_data["followers_id"],
        )
        if not create:
            user.delete()
            return Response(status=202)

        return user

    def validate_user_id(self, value):
        user = User.objects.filter(id=value)
        if not user.first():
            raise ValidationError(detail="User with this ID doesnt exists")

        return user


class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(min_length=10, max_length=50)
    message = serializers.CharField(min_length=10, max_length=150)
    to = serializers.EmailField()

    def validate_to(self, value):
        user = User.objects.filter(email=value)
        if not user.first():
            raise ValidationError(detail="User with this email doesnt exists")

        return value


class NewsLetterSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserEmailNewsLetter
        fields = ["user", "sending_out_offers", "news_mailer"]


class ChangeNewsLetterSerializer(serializers.Serializer):
    sending_out_offers = serializers.BooleanField(required=False)
    news_mailer = serializers.BooleanField(required=False)
