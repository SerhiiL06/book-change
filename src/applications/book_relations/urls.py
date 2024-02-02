from django.urls import path

from . import views

app_name = "book_relations"

urlpatterns = [
    path(
        "add-to-bookmark/<slug:book_slug>/",
        views.add_to_bookmark,
        name="add-to-bookmark",
    ),
    path("rait/", views.left_rating, name="rating"),
    path("my-bookmarks/", views.bookmark_list, name="bookmark-list"),
    path(
        "share/<slug:book_slug>/", views.ShareMessageView.as_view(), name="share-book"
    ),
]
