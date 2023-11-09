from django.urls import path
from . import views

urlpatterns = [
    path("book-list/", views.BookListAPIView.as_view()),
    path("book-list/<int:book_id>/", views.BookDetailAPIView.as_view()),
]
