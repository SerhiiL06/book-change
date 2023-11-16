from django.urls import path

from . import views

urlpatterns = [
    path("book-list/", views.BookListAPIView.as_view()),
    path("book-list/<int:book_id>/", views.BookDetailAPIView.as_view()),
    path("add-comment/", views.CommentAPIView.as_view()),
    path("genre-list/", views.GenreListAPIView.as_view()),
    path("genre-list/<int:genre_id>/", views.GenreDetailAPIView.as_view()),
    path("author-list/", views.AuthorListAPIView.as_view()),
    path("author-list/<int:pk>/", views.AuthorDetailAPIView.as_view()),
]
