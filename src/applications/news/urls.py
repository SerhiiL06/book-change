from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("", views.NewsListView.as_view(), name="news-list"),
    path("like/<int:news_id>/", views.LikeView.as_view(), name="like"),
]
