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
    path("comment/<slug:slug>/", views.DetailBookView.as_view(), name="add-comment"),
]
