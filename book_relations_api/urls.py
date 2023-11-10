from django.urls import path
from . import views

urlpatterns = [
    path("book-relations-list/", views.BookRelationsAPIView.as_view()),
    path(
        "book-relations-list/<int:book_id>/", views.BookRelationsDetailAPIView.as_view()
    ),
]
