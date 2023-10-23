from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    join_at = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    total_books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "join_at",
            "email",
            "total_books",
            "my_books",
            "followers",
        ]

    def get_join_at(self, obj):
        return obj.join_at.date()

    def get_followers(self, obj):
        return obj.followers.count()

    def get_total_books(self, obj):
        return obj.my_books.count()
