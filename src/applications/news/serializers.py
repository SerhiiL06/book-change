from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "text",
            "image",
            "publish",
            "likes",
            "author",
            "created_date",
        ]

    def get_created_date(self, obj):
        return obj.created_date.date()

    def get_author(self, obj):
        return obj.author.full_name()
