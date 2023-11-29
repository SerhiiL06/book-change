from django.db import models

from src.applications.users.models import User


class News(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="news-image/", null=True, blank=True)

    publish = models.BooleanField(default=True)

    likes = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.PROTECT)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_news")
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="likes_user")

    date = models.DateTimeField(auto_now_add=True)
