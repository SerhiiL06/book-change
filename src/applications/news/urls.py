from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("", views.NewsListView.as_view(), name="news-list"),
    path("create-news/", views.CreateNews.as_view(), name="create-news"),
    path("delete/<int:pk>/", views.DeleteNews.as_view(), name="delete-news"),
    path("like/<int:news_id>/", views.LikeView.as_view(), name="like"),
]
