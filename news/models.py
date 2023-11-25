from django.db import models
from users.models import User


class News(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="news-image/", null=True, blank=True)

    publish = models.BooleanField(default=True)

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.PROTECT)
