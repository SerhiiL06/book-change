from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register("", views.ShareBookAPIView)

urlpatterns = [
    path("book-relations-list/", views.BookRelationsAPIView.as_view()),
    path(
        "book-relations-list/<int:book_id>/", views.BookRelationsDetailAPIView.as_view()
    ),
    path("my-bookmark/", views.UserBookmarkListAPIView.as_view()),
]


urlpatterns += router.urls
