from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = "book_request"

urlpatterns = [
    path("send/<int:book_id>/", views.send_book_request, name="send-request"),
    path(
        "my-requests/",
        login_required(views.BookRequestsView.as_view()),
        name="my-requests",
    ),
    path(
        "request/<int:request_id>/",
        views.BookRequestDetailView.as_view(),
        name="request-detail",
    ),
]
