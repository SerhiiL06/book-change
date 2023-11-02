from django.urls import path
from . import views


app_name = "books"


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("search/", views.SearchView.as_view(), name="search"),
    path(
        "book-detail/<slug:slug>/",
        views.DetailBookView.as_view(),
        name="detail-book",
    ),
    path("create-book/", views.CreateBookView.as_view(), name="create-book"),
    path("comment/<slug:slug>/", views.DetailBookView.as_view(), name="add-comment"),
    path("my-books/", views.MyBookListView.as_view(), name="my-books"),
    path("update-book/<int:pk>/", views.UpdateBookView.as_view(), name="update-book"),
    path("delete-book/<int:pk>/", views.delete_book_view, name="delete-book"),
]
