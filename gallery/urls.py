from django.urls import path
from . import views


app_name = "gallery"

urlpatterns = [
    path("", views.GalleryView.as_view(), name="gallery"),
    path("<str:tag_name>/", views.GalleryView.as_view(), name="gallery-with-tag"),
    path("<int:profile_id>/", views.GalleryView.as_view(), name="gallery-user"),
    path("upload-file/", views.UploadImageToGalleryView.as_view(), name="upload-file"),
]
