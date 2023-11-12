from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookRequestListAPIView.as_view()),
    path("<int:request_id>/", views.BookRequestDetailAPIView.as_view()),
]
