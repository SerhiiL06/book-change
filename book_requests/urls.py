from django.urls import path
from . import views


app_name = "book_request"

urlpatterns = [
    path("send/<int:book_id>/", views.send_book_request, name="send-request"),
]
