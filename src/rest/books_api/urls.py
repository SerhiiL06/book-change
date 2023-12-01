from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(r"genre", views.GenreViewSets)
router.register(r"author", views.AuthorViewSet)


urlpatterns = [
    path("book-list/", views.BookListAPIView.as_view()),
    path("book-list/<int:book_id>/", views.BookDetailAPIView.as_view()),
    path("add-comment/", views.CommentAPIView.as_view()),
]


urlpatterns += router.urls
