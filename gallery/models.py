from django.db import models
from users.models import User


class Gallery(models.Model):
    image = models.ImageField(upload_to="gallery_img/")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_upload = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField("ImageTag", related_name="tags")


class ImageTag(models.Model):
    tag_name = models.CharField(max_length=15)

    def __str__(self):
        return self.tag_name
