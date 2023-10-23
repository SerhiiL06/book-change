from django.urls import path
from . import views

app_name = "book_relations"

urlpatterns = [
    path(
        "add-to-bookmark/<slug:book_slug>/",
        views.add_to_bookmark,
        name="add-to-bookmark",
    ),
]
