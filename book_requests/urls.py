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
    path("success-request/", views.get_book_request, name="get-request"),
    path("canceled-request/", views.failed_book_request, name="failed-request"),
    path("history/", views.history_list, name="history"),
]
